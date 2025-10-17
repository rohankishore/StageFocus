"""
Manages the system tray icon and application lifecycle for StageFocus.
"""
import threading
from PIL import Image
from pystray import Icon as TrayIcon, MenuItem as item


def create_tray_icon(stop_event: threading.Event):
    """
    Creates and runs the system tray icon.

    The icon provides an 'Exit' option to gracefully shut down the application.

    Args:
        stop_event: A threading.Event to signal when the application should exit.
    """

    def exit_action(icon):
        """Stops the camera thread and exits the application."""
        print("Exit requested from tray.")
        if not stop_event.is_set():
            stop_event.set()
        icon.stop()

    image = Image.open("stagefocus/icon.jpg")
    menu = (item('Exit', lambda icon, menu_item: exit_action(icon)),)
    icon = TrayIcon("StageFocus", image, "StageFocus - Center Stage", menu)

    print("Starting system tray icon...")
    icon.run()

    # When icon.run() finishes, it means we are exiting.
    if not stop_event.is_set():
        stop_event.set()
    print("System tray icon stopped.")
