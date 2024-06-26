# app/__main__.py
from selenium import webdriver
from app.view_login import ManejadorLogin
from app.view_home import ManejadorHome
from app.utils.configuracion import ConfiguracionSelenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer las variables de entorno
usuario = os.getenv("USUARIO")
contraseña = os.getenv("PASSWORD")

class Scraping_de_Instagram_Ads_Bot:
    URL_INSTAGRAM = "https://www.instagram.com/"

    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña
        self.driver = None

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    

    def start_bot(self, configuracion_selenium):
        try:
            # Configurar el navegador
            self.driver = webdriver.Chrome(options=configuracion_selenium.obtener_opciones())

            # Abrir la URL de Instagram
            self.driver.get(self.URL_INSTAGRAM)

            # Iniciar sesión
            ManejadorLogin(self.driver, self.usuario, self.contraseña).login()

            # Manejadro inicio -> web scrapy
            manejador_inicio = ManejadorHome(self.driver).start_home()

        except Exception as e:
            print(f"Error en el bot: {str(e)}")

if __name__ == "__main__":
    # --------------------------------------- #
    # Ruta relativa
    relative_path = "../Scraping-de-Instagram-Ads/user_data_cache/data"
    absolute_path = os.path.abspath(relative_path)
    user_data_dir = absolute_path
    # --------------------------------------- #
    configuracion_selenium = ConfiguracionSelenium(user_data_dir)
    instagram_bot = Scraping_de_Instagram_Ads_Bot(usuario, contraseña).start_bot(configuracion_selenium)

