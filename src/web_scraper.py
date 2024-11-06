from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class WebScraper:
    def __init__(self, headless=True):
        # Configura el ChromeDriver automáticamente usando webdriver-manager
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Usa ChromeDriverManager para gestionar el driver_path automáticamente
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def cerrar_cookies(self):
        try:
            # Localizar el botón de "Aceptar y cerrar", para cerrar el pop up de Cookies
            boton_aceptar_cookies = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Aceptar y cerrar")]'))
            )
            
            # Hacer clic en el botón de aceptar cookies
            boton_aceptar_cookies.click()
            
            print("Ventana de cookies cerrada.")
        except Exception as e:
            print("No se pudo encontrar el botón de cookies o ya estaba cerrado")

    def navegar_a_listado(self, url):
        # Abre la URL del listado
        self.driver.get(url)
        
        self.cerrar_cookies()

        # Espera hasta que el botón "Ver resultados" esté disponible y haz clic
        try:
            boton_ver_resultados = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Ver') and contains(text(), 'resultados')]"))
            )
            boton_ver_resultados.click()
            print("Botón 'Ver resultados' encontrado y clicado.")
        except:
            print("Botón 'Ver resultados' no encontrado o no es necesario hacer clic.")

    def extraer_datos_listado(self):
        # Espera a que cargue al menos un elemento de propiedad 'ad-preview'
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ad-preview"))
        )

        # Obtén el HTML de la página de resultados
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Encuentra todos los elementos de propiedades directamente
        propiedades = soup.find_all('div', class_='ad-preview')
        
        # Lista para almacenar los datos de cada propiedad
        datos_propiedades = []

        # Extrae la información de cada propiedad
        for propiedad in propiedades:
            try:
                # Precio
                precio = propiedad.find('span', class_='ad-preview__price').get_text(strip=True)

                # Titulo
                titulo = propiedad.find('a', class_='ad-preview__title').get_text(strip=True)

                # Ubicacion
                ubicacion = propiedad.find('p', class_='ad-preview__subtitle').get_text(strip=True)

                # Extraer el número de habitaciones, baños y metros cuadrados
                detalles = propiedad.find_all('p', class_='ad-preview__char')
                habitaciones = detalles[0].get_text(strip=True) if len(detalles) > 0 else "N/A"
                banos = detalles[1].get_text(strip=True) if len(detalles) > 1 else "N/A"
                metros_cuadrados = detalles[2].get_text(strip=True) if len(detalles) > 2 else "N/A"

                # Agregar los datos a la lista
                datos_propiedades.append({
                    "Precio": precio,
                    "Título": titulo,
                    "Ubicación": ubicacion,
                    "Habitaciones": habitaciones,
                    "Baños": banos,
                    "Metros Cuadrados": metros_cuadrados
                })
            except Exception as e:
                print(f"Error al extraer datos de una propiedad: {e}")

        return datos_propiedades

    def pulsar_cerrar_popup(self):
        try:
            # Esperar hasta que el botón con clase 'modal__close' sea clickeable
            boton_cerrar_modal = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.modal__close'))
            )
            
            # Hacer clic en el botón de cerrar modal
            boton_cerrar_modal.click()
            print("Botón 'Cerrar' clickeado correctamente.")
            
        except Exception as e:
            print("No se pudo hacer clic en el botón 'Cerrar'")

    def avanzar_pagina(self, first_page):
        try:
            if first_page:
                # Usar el XPath para seleccionar el div o el enlace dentro del div
                siguiente_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="pagination__next single"]//a'))
                )
            else:
                siguiente_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="pagination__next border-l"]//a'))
                )

            # Hacer clic en el botón "Siguiente"
            siguiente_boton.click()
            print("Botón 'Siguiente' clickeado correctamente.")

        except Exception as e:
            print("No se pudo hacer clic en el botón 'Siguiente'")


    def cerrar(self):
        # Cerrar el navegador
        self.driver.quit()
