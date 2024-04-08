# app/utils/click.py
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
import time

class ClickManager:
    def __init__(self, driver):
        self.driver = driver

    def click(self, elemento):
        intentos = 3  # Número máximo de intentos
        for _ in range(intentos):
            try:
                elemento.click()
                return  # El clic fue exitoso, sal del método
            except (ElementClickInterceptedException, ElementNotInteractableException):
                # Si el clic es interceptado o el elemento no es interactuable, intenta hacer clic usando JavaScript
                self.driver.execute_script("arguments[0].click();", elemento)
                return  # El clic con JavaScript fue exitoso, sal del método
            except Exception as e:
                # Manejar cualquier otra excepción que pueda ocurrir al intentar hacer clic
                # print(f"Error al hacer clic: {e}")
                pass
            
            time.sleep(1)  # Espera un segundo antes de intentar nuevamente
