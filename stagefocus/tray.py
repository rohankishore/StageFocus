"""
Manages the system tray icon and application lifecycle for StageFocus.
"""
import threading
from PIL import Image
from pystray import Icon as TrayIcon, MenuItem as item
from . import settings_ui

def create_tray_icon(config_manager, stop_event: threading.Event):
    """
    Creates and runs the system tray icon.

    The icon provides an 'Exit' option to gracefully shut down the application.

    Args:
        config_manager: An instance of the ConfigManager class.
        stop_event: A threading.Event to signal when the application should exit.
    """

    def exit_action(icon):
        """Stops the camera thread and exits the application."""
        print("Exit requested from tray.")
        if not stop_event.is_set():
            stop_event.set()
        icon.stop()

    def open_settings(icon):
        """Opens the settings window."""
        settings_ui.open_settings_window(config_manager)

    image = Image.open("stagefocus/icon.jpg")
    menu = (
        item('Settings', lambda icon, menu_item: open_settings(icon)),
        item('Exit', lambda icon, menu_item: exit_action(icon))
    )
    icon = TrayIcon("StageFocus", image, "StageFocus - Center Stage", menu)

    print("Starting system tray icon...")
    icon.run()

    # When icon.run() finishes, it means we are exiting.
    if not stop_event.is_set():
        stop_event.set()
    print("System tray icon stopped.")
