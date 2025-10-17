"""
Core computer vision and virtual camera logic for StageFocus.
"""
import cv2
import mediapipe as mp
import numpy as np
import pyvirtualcam
import threading

def run_center_stage(config_manager, stop_event: threading.Event):
    """
    Initializes and runs the main computer vision loop.

    This function captures video from the webcam, uses MediaPipe to detect
    the user's pose, calculates a bounding box to keep the user centered,
    and sends the resulting cropped and resized frame to a virtual camera.

    Args:
        config_manager: An instance of the ConfigManager class.
        stop_event: A threading.Event object to signal when the loop should stop.
    """
    mp_pose = mp.solutions.pose
    pose = mp.solutions.pose.Pose()

    cap = cv2.VideoCapture(config_manager.get("WEBCAM_ID"))
    if not cap.isOpened():
        print("Error: Cannot open video source. Is another app using the camera?")
        return

    source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    source_fps = int(cap.get(cv2.CAP_PROP_FPS))
    if source_fps == 0:
        source_fps = 30

    print(f"Source: {source_width}x{source_height} @ {source_fps} FPS")
    smoothed_box = np.array([0, 0, source_width, source_height], dtype=float)

    try:
        with pyvirtualcam.Camera(width=source_width, height=source_height, fps=source_fps) as cam:
            print(f'Virtual camera "{cam.device}" started.')
            while not stop_event.is_set():
                success, frame = cap.read()
                if not success:
                    break

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    min_x, max_x = source_width, 0
                    min_y, max_y = source_height, 0

                    for landmark in landmarks:
                        if landmark.visibility > 0.5:
                            px, py = int(landmark.x * source_width), int(landmark.y * source_height)
                            min_x, max_x = min(min_x, px), max(max_x, px)
                            min_y, max_y = min(min_y, py), max(max_y, py)

                    box_w, box_h = max_x - min_x, max_y - min_y
                    pad_w, pad_h = int(box_w * config_manager.get("PADDING_FACTOR")), int(box_h * config_manager.get("PADDING_FACTOR"))
                    target_box = np.array([min_x - pad_w, min_y - pad_h, box_w + 2 * pad_w, box_h + 2 * pad_h])
                else:
                    target_box = np.array([0, 0, source_width, source_height])

                smoothing_factor = config_manager.get("SMOOTHING_FACTOR")
                smoothed_box = smoothed_box * (1 - smoothing_factor) + target_box * smoothing_factor
                x, y, w, h = smoothed_box.astype(int)
                x, y = max(0, x), max(0, y)
                w, h = min(source_width - x, w), min(source_height - y, h)

                if w > 0 and h > 0:
                    cropped_frame = frame[y:y + h, x:x + w]
                    output_frame = cv2.resize(cropped_frame, (source_width, source_height))

                    cv2.imshow("StageFocus Preview", output_frame)

                    output_frame_rgb = cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB)
                    cam.send(output_frame_rgb)
                    cam.sleep_until_next_frame()

                if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("StageFocus Preview",
                                                                              cv2.WND_PROP_VISIBLE) < 1:
                    break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera thread stopped and resources released.")
        stop_event.set()
