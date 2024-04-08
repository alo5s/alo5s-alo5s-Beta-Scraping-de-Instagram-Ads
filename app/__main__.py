# app/__main__.py
from selenium import webdriver
from app.view_login import ManejadorLogin
from app.view_home import ManejadorHome
from app.utils.configuracion import ConfiguracionSelenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
            #capabilities = DesiredCapabilities.CHROME.copy()
            capabilities = webdriver.DesiredCapabilities.CHROME.copy()

            #capabilities['acceptInsecureCerts'] = True

            self.driver = webdriver.Chrome(options=configuracion_selenium.obtener_opciones())


            # Abrir la URL de Instagram
            self.driver.get(self.URL_INSTAGRAM)

            # Iniciar sesión
            ManejadorLogin(self.driver, self.usuario, self.contraseña).login()
            # ============== #
            # ============== #
            # Manejadro inicio -> web scrapy

            manejador_inicio = ManejadorHome(self.driver).start_home()
            print("LISTO COMPRUEBE")
            #import time
            #time.sleep(50)
            print("FINAL")

        except Exception as e:
            print(f"Error en el bot: {str(e)}")

if __name__ == "__main__":
    usuario = "jose_testes5"
    contraseña = "testes_123"
    user_data_dir = "/home/angel/Trabajo/Scraping-de-Instagram-Ads/user_data/data_2"
    configuracion_selenium = ConfiguracionSelenium(user_data_dir)
    instagram_bot = Scraping_de_Instagram_Ads_Bot(usuario, contraseña).start_bot(configuracion_selenium)



# josegonzalez.ag002@gmail.com

    """
    gaby valdebenito
    gabyvaldebenito14@gmail.com
    gabrielValdebenito_231

    """
    """
    Perfilse
    ---------------------
    seenkascraper
    1qazZAQ!
    data_1
    ---------------------
    jose_testes5
    testes_123
    """