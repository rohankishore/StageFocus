"""
Main entry point for the StageFocus application.

This script initializes the application, starts the camera and system tray
components in separate threads, and handles graceful shutdown.
"""
import threading
from stagefocus import camera, tray
from stagefocus.config_manager import ConfigManager

def main():
    """
    Initializes and runs the StageFocus application.
    """
    config_manager = ConfigManager()
    stop_event = threading.Event()

    # Start the camera logic in a separate thread
    camera_thread = threading.Thread(target=camera.run_center_stage, args=(config_manager, stop_event,))
    camera_thread.daemon = True

    print("Starting StageFocus...")
    camera_thread.start()

    # Run the system tray icon in the main thread (this is blocking)
    tray.create_tray_icon(config_manager, stop_event)

    # Wait for the camera thread to finish
    print("Waiting for camera thread to shut down...")
    camera_thread.join()

    print("Application has been shut down.")

if __name__ == "__main__":
    main()
