from web_scraper import WebScraper
import time
import csv

if __name__ == "__main__":
    # Se puede cambiar el headless a False para ver el navegador en acción
    scraper = WebScraper(headless=False)

    # URL de ejemplo. En el futuro incorporaremos la busqueda por parametros con la clase Sitemap
    url = "https://www.pisos.com/viviendas/madrid/"
    scraper.navegar_a_listado(url)
    
    aux = 0
    first_page = True
    while aux < 1: # Modificar este número en función de las páginas que se quieran scrapear
        print('Estoy analizando la página: ', aux)

        # Extraer los datos del listado
        propiedades = scraper.extraer_datos_piso()

        # Cerrar un pop up que sale a veces
        scraper.pulsar_cerrar_popup()
        time.sleep(3)

        # Avanzar a la siguiente página
        scraper.avanzar_pagina(first_page)
        first_page = False
        time.sleep(3)

        aux+=1
    
    # Cerrar el navegador
    scraper.cerrar()

    # Imprimir los datos extraídos
    # TODO: De momento solo scrapea los resultados de la primera página, hay que implementar la paginación
    for i, propiedad in enumerate(propiedades, start=1):
        print(f"\nPropiedad {i}:")
        for key, value in propiedad.items():
            print(f"{key}: {value}")

    # Ruta donde se guardará el archivo CSV
    archivo_csv = "dataset/dataset.csv"

    # Escribir los datos en el archivo CSV
    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
        # Crear un escritor CSV que utiliza los diccionarios como entrada
        escritor_csv = csv.DictWriter(file, fieldnames=["Precio", "Título", "Ubicación", "Superficie", "Habitaciones", "Baños", "Planta", "Antigüedad", "Gastos de comunidad", "Referencia"])
        
        # Escribir los encabezados (las claves del diccionario)
        escritor_csv.writeheader()
        
        # Escribir los datos de las propiedades
        escritor_csv.writerows(propiedades)

    print(f"Datos guardados en {archivo_csv}")