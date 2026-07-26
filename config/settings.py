import json
import os

class SettingsManager:

    DEFAULT_SETTINGS = {
    "library_path": "",
    "application": "Music Player",
    "data_structure": "Array",
    "theme": "Dark"
    }

    def __init__(self):
        self.settings_file = os.path.join(
            os.path.dirname(__file__),
            "settings.json"
        )

        self.settings = {}

        self.load()

    def load(self):
        # LOAD SETTINGS FROM JSON FILE

        if not os.path.exists(self.settings_file):
            self.save()
            return

        try:
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        except:
            self.settings = {}

        # FILL MISSING SETTINGS

        for key, value in  self.DEFAULT_SETTINGS.items():
            self.settings.setdefault(key, value)

        self.save()

    def save(self):
        # SAVE SETTINGS TO THE JSON FILE

        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent = 4)

    def get(self, key, default = None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def reset(self):
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save