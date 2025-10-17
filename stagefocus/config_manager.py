"""
Manages loading and saving of application settings from a JSON file.
"""
import json

CONFIG_FILE = "stagefocus/config.json"

class ConfigManager:
    """
    Handles reading from and writing to the config.json file.
    """
    def __init__(self):
        """Initializes the ConfigManager and loads the settings."""
        self.settings = self.load_settings()

    def load_settings(self):
        """Loads settings from config.json, creating it with defaults if it doesn't exist."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Config file not found or invalid. Creating with default settings.")
            default_settings = {
                "WEBCAM_ID": 0,
                "SMOOTHING_FACTOR": 0.07,
                "PADDING_FACTOR": 0.4
            }
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings):
        """Saves the given settings to config.json."""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        self.settings = settings

    def get(self, key):
        """Gets a setting value by key."""
        return self.settings.get(key)

    def set(self, key, value):
        """Sets a setting value by key and saves the config."""
        self.settings[key] = value
        self.save_settings(self.settings)
