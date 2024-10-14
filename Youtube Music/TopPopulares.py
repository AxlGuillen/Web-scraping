from googleapiclient.discovery import build
import pandas as pd
import unidecode  # Necesitarás esta biblioteca para eliminar acentos

# Clave de API (reemplaza con tu propia API key)
api_key = 'AIzaSyB14E76hfuE1ymxgqxkGv8wxPudF4M-4GM'

# Construir el servicio de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

# Hacer la solicitud para obtener los videos más populares en México
request = youtube.videos().list(
    part='snippet,statistics',
    chart='mostPopular',
    regionCode='MX',  # Código de país para México
    videoCategoryId='10',  # Categoría de música
    maxResults=100  # Número de resultados que quieres obtener
)

response = request.execute()

# Lista para almacenar los datos
data = []

# Imprimir los títulos de los videos y sus artistas
for item in response['items']:
    titulo = item['snippet']['title']
    canal = item['snippet']['channelTitle']
    vistas = item['statistics']['viewCount']
    
    # Eliminar acentos
    titulo_sin_acentos = unidecode.unidecode(titulo)
    canal_sin_acentos = unidecode.unidecode(canal)

    # Agregar los datos a la lista
    data.append({
        'Titulo': titulo_sin_acentos,
        'Artista/Canal': canal_sin_acentos,
        'Vistas': vistas
    })

# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Exportar el DataFrame a un archivo CSV
df.to_csv('1videos_mas_populares_mexico.csv', index=False)

print("Datos exportados a 1videos_mas_populares_mexico.csv")
