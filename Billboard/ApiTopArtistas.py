import billboard
import csv

# Función para obtener los top artistas del Billboard Hot 100 y guardar en CSV
def get_hot_100_artists():
    chart = billboard.ChartData('hot-100')
    artists_count = {}

    # Contamos la cantidad de canciones de cada artista en el Hot 100
    for song in chart:
        artist = song.artist
        if artist in artists_count:
            artists_count[artist] += 1
        else:
            artists_count[artist] = 1

    # Ordenamos por número de apariciones
    top_artists = sorted(artists_count.items(), key=lambda x: x[1], reverse=True)

    # Guardamos en un archivo CSV
    with open('hot_100_artists.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Artist', 'Song Count'])
        for i, (artist, count) in enumerate(top_artists[:100], start=1):
            writer.writerow([i, artist, count])

    print("Hot 100 Artists guardado en hot_100_artists.csv")

# Función para obtener los top artistas del Billboard Artist 100 y guardar en CSV
def get_artist_100():
    import requests
    from bs4 import BeautifulSoup
    import csv

    # URL de la lista Artist 100 de Billboard
    url = 'https://www.billboard.com/charts/artist-100/'

    # Headers para simular un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Realizamos la solicitud con headers
    response = requests.get(url, headers=headers)

    # Verificamos si la solicitud fue exitosa
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        artist_data = []
        rank = 1  # Inicializamos el contador para los artistas

        # Extraemos los contenedores principales de cada artista
        artist_containers = soup.select('.o-chart-results-list-row-container')
        
        # Procesamos cada contenedor de artista
        for container in artist_containers:
            # Extraemos el nombre del artista
            artist_name = container.select_one('h3.c-title').get_text(strip=True)
            
            # Filtramos entradas no deseadas
            if artist_name.lower() != "imprint/promotion label:":
                # Extraemos la lista <ul> con los datos de Last Week, Peak Pos., y Wks on Chart
                stats = container.select('ul.lrv-a-unstyle-list li span')
                
                # Accedemos a los elementos de Last Week, Peak Pos., y Wks on Chart en orden
                last_week_text = stats[0].get_text(strip=True) if len(stats) > 0 else "N/A"
                peak_pos_text = stats[1].get_text(strip=True) if len(stats) > 1 else "N/A"
                wks_on_chart_text = stats[2].get_text(strip=True) if len(stats) > 2 else "N/A"
                
                # Añadimos los datos a la lista en el formato correcto
                artist_data.append((rank, artist_name, last_week_text, peak_pos_text, wks_on_chart_text))
                rank += 1  # Incrementamos solo al agregar un artista válido

                # Detenemos el bucle después de los primeros 100 artistas válidos
                if rank > 100:
                    break

        # Guardamos en un archivo CSV
        with open('artist_100.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Rank', 'Artist', 'Last Week', 'Peak Pos.', 'Wks on Chart'])
            writer.writerows(artist_data)

        print("Artist 100 guardado en artist_100.csv")
    else:
        print(f"Error al acceder a la página: {response.status_code}")





# Ejecutamos las funciones
get_hot_100_artists()
get_artist_100()
