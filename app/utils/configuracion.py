# app/utils/configuracion_selenium.py
from selenium import webdriver

class ConfiguracionSelenium:
    def __init__(self, user_data_dir=None):
        self.options = webdriver.ChromeOptions()
        self.user_data_dir = user_data_dir
        self.establecer_opciones()

    def establecer_opciones(self):
        self.options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.password_manager_enabled": False,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "credentials_enable_autosignin": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": False,
            "safebrowsing.disable_download_protection": True,
            "password_manager_enabled": False,
            "download.default_directory": "/home/angel/Trabajo/Scraping-de-Instagram-Ads/temp/video", # linux / # wind \
            #"intl.accept_languages": "en-US,en"
            "exit_type": "None"  
        })
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument('--log-level=3')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument("--disable-save-password-bubble")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-infobars') 
        if self.user_data_dir:
            self.options.add_argument(f"user-data-dir={self.user_data_dir}")

    def obtener_opciones(self):
        return self.options