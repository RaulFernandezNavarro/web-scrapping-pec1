import requests
from bs4 import BeautifulSoup

class Sitemap:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        self.urls_por_categoria = {
            "Venta por ubicación": [],
            "Alquiler por ubicación": []
        }
    
    def fetch_sitemap(self):
        # Realiza una solicitud GET a la URL del sitemap
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            # Analiza el contenido HTML de la respuesta
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encuentra todas las secciones de la página que contienen enlaces
            secciones = soup.find_all('div', class_='column quarter')
            
            for seccion in secciones:
                # Verifica si la sección es de "Venta por ubicación"
                if seccion.find('div', class_='title') and "Venta por ubicación" in seccion.find('div', class_='title').get_text():
                    # Encuentra todos los enlaces de venta
                    enlaces_venta = seccion.find_all('a', class_='item')
                    for enlace in enlaces_venta:
                        texto = enlace.get_text(strip=True)
                        href = enlace.get('href')
                        if href:
                            # Completa la URL si es relativa
                            href = f"https://www.pisos.com{href}" if href.startswith('/') else href
                            self.urls_por_categoria["Venta por ubicación"].append((texto, href))
                
                # Verifica si la sección es de "Alquiler por ubicación"
                elif seccion.find('div', class_='title') and "Alquiler por ubicación" in seccion.find('div', 'title').get_text():
                    # Encuentra todos los enlaces de alquiler
                    enlaces_alquiler = seccion.find_all('a', class_='item')
                    for enlace in enlaces_alquiler:
                        texto = enlace.get_text(strip=True)
                        href = enlace.get('href')
                        if href:
                            # Completa la URL si es relativa
                            href = f"https://www.pisos.com{href}" if href.startswith('/') else href
                            self.urls_por_categoria["Alquiler por ubicación"].append((texto, href))
        else:
            print(f"Error al acceder al mapa del sitio: {response.status_code}")
    
    def get_urls_por_categoria(self):
        # Devuelve las URLs categorizadas
        return self.urls_por_categoria
    
    def search(self, category, keyword):
        # Busca enlaces en una categoría específica que contengan la palabra clave
        results = []
        if category in self.urls_por_categoria:
            for texto, link in self.urls_por_categoria[category]:
                if keyword.lower() in texto.lower():
                    results.append((texto, link))
        return results
