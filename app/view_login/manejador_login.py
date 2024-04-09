from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from app.utils.click import ClickManager
import time

class ManejadorLogin:
    SUSPENDED_PAGE_IDENTIFIER = "https://www.instagram.com/accounts/suspended/"
    #HOME_PAGE_IDENTIFIER = ".x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib"
    HOME_PAGE_IDENTIFIER = "div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib"

    USERNAME = "username"
    PASSWORD = "password"
    BTN_INICIAR_SESION = "button._acan._acap._acas._aj1-._ap30"
    MENSJAE_GUARDAR = ".x1qjc9v5.x9f619.x1roi4f4.x78zum5.xdt5ytf.x2lah0s.xln7xf2.xk390pu.x1aawmmo.x11i5rnm.x1fqp7bg.x1mh8g0r.x1n2onr6.x11njtxf"
    BOTON_GUARDAR = "button._acan._acap._acas._aj1-._ap30"

    def __init__(self, driver, usuario, contraseña):
        self.driver = driver
        self.usuario = usuario
        self.contraseña = contraseña
        self.wait_time = 5

    # Un error para testes y Observación 
    def is_logged_in(self):
        #try:
        self.driver.find_elements(By.CLASS_NAME, self.HOME_PAGE_IDENTIFIER)
            #return True
        #except NoSuchElementException:
        #    return False

    def is_account_suspended(self):
        return self.SUSPENDED_PAGE_IDENTIFIER in self.driver.current_url

    def wait_until_visible(self, by, selector, message="Elemento no visible"):
        return WebDriverWait(self.driver, self.wait_time).until(
            EC.visibility_of_element_located((by, selector)),
            message=message
        )

    def wait_until_clickable(self, by, selector, message="Elemento no clickeable"):
        return WebDriverWait(self.driver, self.wait_time).until(
            EC.element_to_be_clickable((by, selector)),
            message=message
        )

    def login(self):
        if self.is_account_suspended():
            print("¡Cuenta suspendida!")
            return

        if self.is_logged_in():
            print("Ya has iniciado sesión previamente.")
            return

        self.perform_login_actions()
        time.sleep(10)
        self.save_login_data()

    def perform_login_actions(self):
        try:
            campo_usuario = self.wait_until_visible(By.NAME, self.USERNAME, "Campo de usuario no presente")
            campo_contraseña = self.wait_until_visible(By.NAME, self.PASSWORD, "Campo de contraseña no presente")

            campo_usuario.send_keys(self.usuario)
            campo_contraseña.send_keys(self.contraseña)

            boton_iniciar_sesion = self.wait_until_clickable(By.CSS_SELECTOR, self.BTN_INICIAR_SESION, "Botón de iniciar sesión no presente o no clickeable")
            click_manager = ClickManager(self.driver)
            click_manager.click(boton_iniciar_sesion)

        except TimeoutException:
            print("Tiempo de espera agotado al buscar elementos de inicio de sesión")
        except Exception as e:
            print(f"Error durante el inicio de sesión: {str(e)}")

    def save_login_data(self):
        try:
            mensaje_guardar = self.wait_until_visible(By.CSS_SELECTOR, self.MENSJAE_GUARDAR, "Mensaje de guardar información no presente")

            if mensaje_guardar.is_displayed():
                boton_guardar = self.wait_until_clickable(By.CSS_SELECTOR, self.BOTON_GUARDAR, "Botón de guardar no presente o no clickeable")
                click_manager = ClickManager(self.driver)
                click_manager.click(boton_guardar)

        except TimeoutException:
            print("El mensaje de guardar información no se mostró dentro del tiempo de espera.")
        except Exception as e:
            print(f"Error al intentar guardar información de inicio de sesión: {str(e)}")
