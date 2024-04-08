# app/view_home/home.py
import os
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import base64
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import json
from app.utils.click import ClickManager


class ManejadorHome:
    ELEMENTO_SCROLL = "_aalg"
    ELEMENTO_DIV_SCRAPY = "div.x78zum5.xdt5ytf.x5yr21d.xa1mljc.xh8yej3.x1bs97v6.x1q0q8m5.xso031l.x11aubdm.xnc8uc2"

    def __init__(self, driver):
        self.driver = driver
        self.wait_time = 35  # Tiempo de espera por defecto
        
        script_file_path = '/home/angel/Trabajo/Scraping-de-Instagram-Ads/app/utils/grabar_video.js'
        with open(script_file_path, 'r') as file:
            self.script = file.read()

    def download_imagen(self, src):
        if src:
            try:
                url_path = urlparse(src).path
                filename = os.path.basename(url_path)
                filepath = os.path.join('temp', filename)
                os.makedirs('temp', exist_ok=True)
                response = requests.get(src)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            except Exception as e:
                print("Error al descargar o convertir el archivo:", e)
        else:
            print("La URL de origen está vacía. No se puede descargar el archivo.")
    
    def obtener_detalles_publidad_video(self, soup, elemento):
        # Buscar el span que contiene el texto de la publicidad
        span = soup.find('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade') or soup.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
        titulo = span.text if span else None

        # Buscar la URL de la publicación
        url_publicacion = soup.find('a', class_="_ad63")["href"] if soup.find('a', class_="_ad63") else None

        # Buscar la descripción de la publicación
        descripcion_element = soup.find('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
        descripcion = descripcion_element.text if descripcion_element else None

        # Para el total de reproducciones
        try:
            elemento_reproducciones = soup.select_one('section.xat24cr span.xdj266r')
            texto_reproducciones = elemento_reproducciones.text
            total_reproducciones = texto_reproducciones.split()[0]
        except Exception as e:
            total_reproducciones = "0"

        # Para el número de comentarios
        try:        
            elemento_comentarios = soup.select_one('div.x9f619 span.xdj266r')
            texto_comentarios = elemento_comentarios.text
            total_comentarios = texto_comentarios.split()[0]
        except Exception as e:
            total_comentarios = "0"

        return titulo, url_publicacion, descripcion, total_reproducciones, total_comentarios

    def obtener_detalles_publidad_img(self, soup,elemento):
        """
        Si es una publicidad, obtiene los detalles como quién la publicó,
        la URL de la publicidad y más.
        """
        # Buscar el span que contiene el texto de la publicidad
        span = soup.find('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade') or soup.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
        titulo = span.text if span else None

        # Buscar la URL de la publicación
        url_publicacion = soup.find('a', class_="_ad63")["href"] if soup.find('a', class_="_ad63") else None

        # Buscar la descripción de la publicación
        descripcion_element = soup.find('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
        descripcion = descripcion_element.text if descripcion_element else None


        # Para el total de Me gustas de la imge
        try:
            elemento_total_like = soup.select_one('section.xat24cr span.xdj266r')
            texto_total_like = elemento_reproducciones.text
            total_like = texto_total_like.split()[0]
        except Exception as e:
            total_like = "0"

        # Para el número de comentarios
        try:        
            elemento_comentarios = soup.select_one('div.x9f619 span.xdj266r')
            texto_comentarios = elemento_comentarios.text
            total_comentarios = texto_comentarios.split()[1]
        except Exception as e:
            total_comentarios = "0"

        return titulo, url_publicacion, descripcion, total_like , total_comentarios




    def verificar_tipo_elemento(self, elemento):
        """
        Verifica si el elemento es una publicidad o una publicación.
        """
        try:
            # Convierte el elemento a un objeto BeautifulSoup
            soup = BeautifulSoup(elemento.get_attribute('outerHTML'), 'html.parser')

            # Busca el elemento span dentro del elemento proporcionado
            span = soup.find("span", class_="x1fhwpqd x132q4wb x5n08af")
            if span and span.text.strip() == "Publicidad":
                return "Publicidad"
            else:
                return "Publicación"
        except Exception as e:
            print("Error al verificar el tipo de elemento:", e)
            return "Desconocido"
    # Beta
    def guardar_datos_imagen_en_txt(self, tipo_elemento, titulo, url_publicacion, descripcion, total_me_gusta, total_comentarios, lista_url):
        with open('datos_publicidad_imagenes.txt', 'a', encoding='utf-8') as file:
            file.write("==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ====================================================\n")
            file.write("==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ====================================================\n")
            file.write(" ")
            file.write(f"Tipo de elemento: {tipo_elemento} | Tipo: Imagen\n")
            file.write(f"Publicado Por: {titulo}\n")
            file.write(f"{'URL: ' + url_publicacion if url_publicacion else 'No tiene URL'}\n")
            file.write(f"Descripción: {'No tiene descripción' if not descripcion else descripcion}\n")
            file.write(f"El total de Me gusta es: {total_me_gusta}\n")
            file.write(f"El total de Comentarios es: {total_comentarios}\n")
            file.write("URLs de las imágenes:\n")
            for idx, url in enumerate(lista_url, start=1):
                file.write(f"Imagen {idx}: {url}\n")
            file.write("==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ====================================================\n")
            file.write("==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ==================================================== ====================================================\n")

    # Beta
    def guardar_datos_video_en_txt(self, tipo_elemento, titulo, url_publicacion, descripcion, total_reproducciones, numero_comentarios):
        with open('datos_publicidad_videos.txt', 'a', encoding='utf-8') as file:
            file.write(f"Tipo de elemento: {tipo_elemento} | Tipo: Video\n")
            file.write(f"Publicado Por: {titulo}\n")
            file.write(f"{'URL: ' + url_publicacion if url_publicacion else 'No tiene URL'}\n")
            file.write(f"Descripción: {'No tiene descripción' if not descripcion else descripcion}\n")
            file.write(f"El total de Reproducciones es: {total_reproducciones}\n")
            file.write(f"El total de Comentarios es: {numero_comentarios}\n")
            file.write("====================================================\n")

    def scrapy(self, article):
        """
        Un input article
        Valida si es una publicidad o una publicación.
        Valida si tien la opcion para ver mas(FALTA Y AJUSTE)

        """
        container_div_detalle = article.find_elements(By.CSS_SELECTOR, self.ELEMENTO_DIV_SCRAPY)

        for elemento in container_div_detalle:
            tipo_elemento = self.verificar_tipo_elemento(elemento)
            ActionChains(self.driver).move_to_element(elemento).perform()
            try:
                boton_mas = elemento.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='más']")
                self.driver.execute_script("arguments[0].click();", boton_mas)
                time.sleep(0.5)
            except NoSuchElementException:
                pass
            
            #print("Tipo de elemento:", tipo_elemento)

            if tipo_elemento == "Publicidad":
                # Buscar div_contenedor que contiene videos
                div_container_videos = elemento.find_elements(By.CSS_SELECTOR, '.x5yr21d.x1uhb9sk.xh8yej3')
                for container in div_container_videos:
                    #print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Video")
                    videos = container.find_elements(By.TAG_NAME, 'video')
                    
                    for video in videos:
                        self.driver.execute_script(self.script)
                        time.sleep(2)
                        #boton_grabar_video = elemento.find_element(By.CLASS_NAME, "Dowloader")
                        #boton_grabar_video.click()
                        #WebDriverWait(elemento, 400).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "Dowloader"), "Listo"))
                        #print("El botón ha cambiado a 'Listo'")
                    
                    soup = BeautifulSoup(elemento.get_attribute('outerHTML'), 'html.parser')
                    titulo, url_publicacion, descripcion, total_reproducciones, numero_comentarios  = self.obtener_detalles_publidad_video(soup, elemento)
                    self.guardar_datos_video_en_txt(tipo_elemento, titulo, url_publicacion, descripcion, total_reproducciones, numero_comentarios)

                    #print("====================================================")
                    #print("Publicado Por:", titulo)
                    #print(url_publicacion)
                    #print(descripcion)
                    #print("El total de Reproducciones es:", total_reproducciones)
                    #print("El total de Comentarios es:", numero_comentarios)
                    #print("====================================================")

                div_container_images = elemento.find_elements(By.CSS_SELECTOR, 'div._aagu')
                for container in div_container_images:
                    print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Imagenes")
                    while True:
                        try:
                            # Encontrar el botón "Siguiente" si está presente
                            next_button = container.find_element(By.CSS_SELECTOR, 'button._afxw._al46._al47')
                            if next_button.is_displayed():
                                # Hacer clic en el botón "Siguiente"
                                next_button.click()
                            else:
                                break  # Salir del bucle si el botón no está visible
                        except:
                            break  

                    # Encontrar todas las imágenes dentro del contenedor
                    images = container.find_elements(By.TAG_NAME, 'img')    
                    lista_url = []
                    for img in images:
                        src = img.get_attribute('src')
                        if src:
                            lista_url.append(src)
                    
                    soup = BeautifulSoup(elemento.get_attribute('outerHTML'), 'html.parser')
                    titulo, url_publicacion, descripcion, total_me_gusta , total_comentarios = self.obtener_detalles_publidad_img(soup, elemento)
                    self.guardar_datos_imagen_en_txt(tipo_elemento, titulo, url_publicacion, descripcion, total_me_gusta, total_comentarios, lista_url)

                    #print("====================================================")
                    #print("Publicado Por:", titulo)
                    #print(url_publicacion)
                    #print(descripcion)
                    #print("El total de Me gusta es:", total_me_gusta)
                    #print("El total de Comentarios es:", total_comentarios)
                    #print("====================================================")
                    
            elif tipo_elemento == "Publicación":
                print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Publicación")

    def scroll(self):
        try:
            elemento_scroll = WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.ELEMENTO_SCROLL)),
                message="El elemento de scroll no está presente."
            )

            current_scroll_position = self.driver.execute_script("return window.scrollY")
            document_height = self.driver.execute_script("return document.body.scrollHeight")

            target_scroll_position = random.uniform(current_scroll_position, document_height)

            while current_scroll_position < target_scroll_position:
                current_scroll_position += random.uniform(100, 150)  
                if current_scroll_position > target_scroll_position:
                    current_scroll_position = target_scroll_position
                self.driver.execute_script("window.scrollTo(0, arguments[0]);", current_scroll_position)
                time.sleep(random.uniform(0.1, 0.3))  

            self.driver.execute_script("window.scrollBy(0, 1);")
            time.sleep(random.uniform(0.1, 0.3))  

        except TimeoutException as e:
            print("Tiempo de espera excedido:", e)
        except Exception as e:
            print("Ocurrió un error:", e)


    def click_articulos(self):
        try:
            elementos_clicados = set()
            clics_realizados = 0  
            while clics_realizados < 100: 
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "x9f619"))
                )

                contenedor_articulos = self.driver.find_element(By.CLASS_NAME, "x9f619")

                articulos = contenedor_articulos.find_elements(By.TAG_NAME, "article")
                # Btn de mute "Obsoleto"
                #boton_audio = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Activar o desactivar audio"]')
                #self.driver.execute_script("arguments[0].click();", boton_audio)
                
                for articulo in articulos:
                    if articulo not in elementos_clicados:
                        ActionChains(self.driver).move_to_element(articulo).perform()
                        ClickManager(articulo)
                        time.sleep(2)
                        self.scrapy(articulo)
                        elementos_clicados.add(articulo)
                        clics_realizados += 1  
                        time.sleep(1)

        except TimeoutException as e:
            print("Tiempo de espera excedido:", e)
        except Exception as e:
            print("Ocurrió un error:", e)

    def start_home(self):
        print("====================================================")
        self.click_articulos()
        print("compruebe los datos")
        time.sleep(100)


