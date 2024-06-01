import json

class SettingsManager():
    """
    Manages the caching the settings in a json file
    """

    def __init__(self, settings_path='settings.json'):
        self.settings_path = settings_path
        self.settings = self.load_settings() 

    def load_settings(self):
        with open(self.settings_path, 'r') as f:
            return json.load(f)

    def save_settings(self):
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_listings(self):
        return self.settings.get('listings', [])

    def set_listings(self, listings):
        self.settings['listings'] = listings
        self.save_settings()

    def valid_settings(self):
        if self.settings['webhook'] == "":
            return False
        if len(self.settings['listings']) == 0:
            return False
        return True
