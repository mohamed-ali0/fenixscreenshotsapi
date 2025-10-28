import json
import os


class SystemSettings:
    """Manages system settings stored in a JSON file"""
    
    SETTINGS_FILE = "system_settings.json"
    
    DEFAULT_SETTINGS = {
        "frequency_hours": 24,  # Default: once a day
        "preferred_hour": 10,   # Default: 10 AM Central USA
        "admin_password": "YB02Ss3JJdk",
        "login_credentials": {
            "username": "sara@fouroneone.io",
            "password": "Ss925201!"
        }
    }
    
    def __init__(self):
        """Initialize settings, create file if it doesn't exist"""
        if not os.path.exists(self.SETTINGS_FILE):
            self._save_settings(self.DEFAULT_SETTINGS)
    
    def _load_settings(self):
        """Load settings from file"""
        try:
            with open(self.SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.DEFAULT_SETTINGS.copy()
    
    def _save_settings(self, settings):
        """Save settings to file"""
        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_frequency(self):
        """Get screenshot frequency in hours"""
        settings = self._load_settings()
        return settings.get("frequency_hours", self.DEFAULT_SETTINGS["frequency_hours"])
    
    def set_frequency(self, hours):
        """Set screenshot frequency in hours"""
        settings = self._load_settings()
        settings["frequency_hours"] = hours
        return self._save_settings(settings)
    
    def verify_admin_password(self, password):
        """Verify admin password"""
        settings = self._load_settings()
        return settings.get("admin_password") == password
    
    def get_login_credentials(self):
        """Get login credentials for the portal"""
        settings = self._load_settings()
        return settings.get("login_credentials", self.DEFAULT_SETTINGS["login_credentials"])
    
    def set_login_credentials(self, username, password):
        """Set login credentials for the portal"""
        settings = self._load_settings()
        settings["login_credentials"] = {
            "username": username,
            "password": password
        }
        return self._save_settings(settings)
    
    def get_preferred_hour(self):
        """Get preferred hour for scheduled captures (0-23)"""
        settings = self._load_settings()
        return settings.get("preferred_hour", self.DEFAULT_SETTINGS["preferred_hour"])
    
    def set_preferred_hour(self, hour):
        """Set preferred hour for scheduled captures (0-23)"""
        if not isinstance(hour, int) or hour < 0 or hour > 23:
            raise ValueError("Hour must be an integer between 0 and 23")
        settings = self._load_settings()
        settings["preferred_hour"] = hour
        return self._save_settings(settings)
    
    def get_all_settings(self, include_passwords=False):
        """Get all settings (optionally hide passwords)"""
        settings = self._load_settings()
        if not include_passwords:
            settings = settings.copy()
            settings["admin_password"] = "***"
            settings["login_credentials"]["password"] = "***"
        return settings


if __name__ == "__main__":
    # Test the settings manager
    settings = SystemSettings()
    print("Current settings:", settings.get_all_settings())
    print("Frequency:", settings.get_frequency(), "hours")
    print("Login username:", settings.get_login_credentials()["username"])
    print("Admin password valid:", settings.verify_admin_password("YB02Ss3JJdk"))


