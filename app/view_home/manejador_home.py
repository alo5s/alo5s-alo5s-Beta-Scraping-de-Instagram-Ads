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
from app.utils.click import ClickManager


class ManejadorHome:
    ELEMENTO_SCROLL = "_aalg"
    ELEMENTO_DIV_SCRAPY = "div.x78zum5.xdt5ytf.x5yr21d.xa1mljc.xh8yej3.x1bs97v6.x1q0q8m5.xso031l.x11aubdm.xnc8uc2"

    def __init__(self, driver):
        self.driver = driver
        self.wait_time = 35

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
    
    
    def obtener_detalles_publicidad(self, soup, elemento):

        span = soup.find('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade') or soup.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
        titulo = span.text if span else None

        url_publicacion = soup.find('a', class_="_ad63")["href"] if soup.find('a', class_="_ad63") else None

        descripcion_element = soup.find('span', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
        descripcion = descripcion_element.text if descripcion_element else None

        return titulo, url_publicacion, descripcion


    def obtener_detalles_publicidad_video(self, soup, elemento):
        titulo, url_publicacion, descripcion = self.obtener_detalles_publicidad(soup, elemento)
        try:
            elemento_reproducciones = soup.select_one('section.xat24cr span.xdj266r')
            texto_reproducciones = elemento_reproducciones.text
            total_reproducciones = elemento_reproducciones.text.split()[0]
        except Exception as e:
            total_reproducciones = "0"

        try:        
            elemento_comentarios = soup.select_one('div.x9f619 span.xdj266r')
            texto_comentarios = elemento_comentarios.text
            total_comentarios = texto_comentarios.split()[0]
        except Exception as e:
            total_comentarios = "0"

        return titulo, url_publicacion, descripcion, total_reproducciones, total_comentarios


    def obtener_detalles_publicidad_img(self, soup, elemento):
        titulo, url_publicacion, descripcion = self.obtener_detalles_publicidad(soup, elemento)
        total_like = "0"
        total_comentarios = "0"

        try:
            elemento_total_like = soup.select_one('section.xat24cr span.x1vvkbs')
            if elemento_total_like:
                texto_total_like = elemento_total_like.text
                total_like = texto_total_like.split()[0]
        except Exception as e:
            print("Error al obtener el total de Me gusta:", e)

        try:
            elemento_comentarios = soup.select_one('div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1xmf6yo.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 span.xdj266r')
            if elemento_comentarios:
                texto_comentarios = elemento_comentarios.text
                total_comentarios = texto_comentarios.split()[0]
        except Exception as e:
            print("Error al obtener el total de comentarios:", e)

        return titulo, url_publicacion, descripcion, total_like, total_comentarios

    def verificar_tipo_elemento(self, elemento):
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
            #if mode == 'w':
            file.write("====================================================\n")
            file.write(f"Tipo de elemento: {tipo_elemento} | Tipo: Imagen\n")
            file.write(f"Publicado Por: {titulo}\n")
            file.write(f"{'URL: ' + url_publicacion if url_publicacion else 'No tiene URL'}\n")
            file.write(f"Descripción: {'No tiene descripción' if not descripcion else descripcion}\n")
            file.write(f"El total de Me gusta es: {total_me_gusta}\n")
            file.write(f"El total de Comentarios es: {total_comentarios}\n")
            file.write("URLs de las imágenes:\n")
            for idx, url in enumerate(lista_url, start=1):
                file.write(f"Imagen {idx}: {url}\n")
            #if mode == 'w':
            file.write("====================================================\n")

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
            
            if tipo_elemento == "Publicidad":
                # Buscar div_contenedor que contiene videos
                div_container_videos = elemento.find_elements(By.CSS_SELECTOR, '.x5yr21d.x1uhb9sk.xh8yej3')
                for container in div_container_videos:
                    #print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Video")
                    videos = container.find_elements(By.TAG_NAME, 'video')
                    
                    for video in videos:
                        pass
                    
                    soup = BeautifulSoup(elemento.get_attribute('outerHTML'), 'html.parser')
                    detalles = self.obtener_detalles_publicidad_video(soup, elemento)
                    self.guardar_datos_video_en_txt(tipo_elemento, *detalles)

                div_container_images = elemento.find_elements(By.CSS_SELECTOR, 'div._aagu')
                for container in div_container_images:
                    print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Imagenes")

                    # Encontrar todas las imágenes dentro del contenedor
                    images = container.find_elements(By.TAG_NAME, 'img')    
                    lista_url = []
                    for img in images:
                        src = img.get_attribute('src')
                        if src:
                            lista_url.append(src)
                    
                    soup = BeautifulSoup(elemento.get_attribute('outerHTML'), 'html.parser')
                    detalles = self.obtener_detalles_publicidad_img(soup, elemento)
                    self.guardar_datos_imagen_en_txt(tipo_elemento, *detalles, lista_url)

            elif tipo_elemento == "Publicación":
                print("Tipo de elemento:", tipo_elemento, " |   Tipo:", "Publicación")

    def click_articulos(self):
        try:
            elementos_clicados = set()
            clics_realizados = 0  
            while clics_realizados < 20: 
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "x9f619"))
                )

                contenedor_articulos = self.driver.find_element(By.CLASS_NAME, "x9f619")

                articulos = contenedor_articulos.find_elements(By.TAG_NAME, "article")

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
        self.click_articulos()

