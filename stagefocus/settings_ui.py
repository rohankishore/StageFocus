"""
Creates a lightweight UI for adjusting application settings.
"""
import tkinter as tk
from tkinter import ttk

class SettingsUI:
    """
    A Tkinter window for viewing and editing application settings.
    """
    def __init__(self, config_manager):
        """Initializes the settings window."""
        self.config_manager = config_manager
        self.window = tk.Tk()
        self.window.title("StageFocus Settings")

        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        """Creates the UI widgets for the settings window."""
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.entries = {}
        settings = self.config_manager.load_settings()

        for i, (key, value) in enumerate(settings.items()):
            label = ttk.Label(frame, text=key)
            label.grid(row=i, column=0, sticky=tk.W, pady=5)

            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
            self.entries[key] = entry

        save_button = ttk.Button(frame, text="Save", command=self.save_settings)
        save_button.grid(row=len(settings), column=0, columnspan=2, pady=10)

    def load_settings(self):
        """Loads the current settings into the UI fields."""
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.config_manager.get(key))

    def save_settings(self):
        """Saves the settings from the UI fields to the config file."""
        for key, entry in self.entries.items():
            try:
                # Attempt to convert to float, then int if it's a whole number
                value = float(entry.get())
                if value.is_integer():
                    value = int(value)
                self.config_manager.set(key, value)
            except ValueError:
                # If conversion fails, save as string
                self.config_manager.set(key, entry.get())
        self.window.destroy()

    def run(self):
        """Displays the settings window."""
        self.window.mainloop()

def open_settings_window(config_manager):
    """Function to be called from the tray menu to open the settings UI."""
    ui = SettingsUI(config_manager)
    ui.run()
