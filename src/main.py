from web_scraper import WebScraper

if __name__ == "__main__":
    # Se puede cambiar el headless a False para ver el navegador en acción
    # TODO: Con headless en false de momento el popup de cookies no se cierra automáticamente, hay que hacerlo manualmente
    scraper = WebScraper(headless=True)

    # URL de ejemplo. En el futuro incorporaremos la busqueda por parametros con la clase Sitemap
    url = "https://www.pisos.com/viviendas/madrid/"
    scraper.navegar_a_listado(url)
    
    # Extraer los datos del listado
    propiedades = scraper.extraer_datos_listado()
    
    # Cerrar el navegador
    scraper.cerrar()

    # Imprimir los datos extraídos
    # TODO: De momento solo scrapea los resultados de la primera página, hay que implementar la paginación
    for i, propiedad in enumerate(propiedades, start=1):
        print(f"\nPropiedad {i}:")
        for key, value in propiedad.items():
            print(f"{key}: {value}")
