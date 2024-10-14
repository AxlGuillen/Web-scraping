from googleapiclient.discovery import build
import pandas as pd
import unidecode

# Clave de API (reemplaza con tu propia API key)
api_key = 'AIzaSyB14E76hfuE1ymxgqxkGv8wxPudF4M-4GM'

# Función para buscar el canal del artista
def buscar_canal(artista):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Hacer la solicitud para buscar el canal
    request = youtube.search().list(
        q=artista,
        part='id,snippet',
        type='channel',
        maxResults=1  # Solo queremos un resultado
    )
    response = request.execute()
    
    # Obtener el ID del canal
    canal_id = response['items'][0]['id']['channelId']
    return canal_id

# Función para obtener videos del canal
def obtener_videos(canal_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Hacer la solicitud para obtener los videos del canal
    request = youtube.search().list(
        part='snippet',
        channelId=canal_id,
        order='viewCount',
        maxResults=100  # Puedes ajustar el número de resultados
    )
    response = request.execute()
    
    return response['items']

# Función para obtener estadísticas de los videos
def obtener_estadisticas_videos(video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Hacer la solicitud para obtener las estadísticas de los videos
    request = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)
    )
    response = request.execute()
    
    return response['items']

# Función principal
def main():
    artista = input("Ingresa el nombre del artista: ")
    canal_id = buscar_canal(artista)
    
    print(f"ID del canal encontrado: {canal_id}")
    
    videos = obtener_videos(canal_id)
    
    # Lista para almacenar los datos
    data = []
    
    # Obtener los IDs de los videos
    video_ids = [item['id']['videoId'] for item in videos if 'videoId' in item['id']]
    
    # Obtener estadísticas de los videos
    estadisticas = obtener_estadisticas_videos(video_ids)

    # Imprimir los títulos de los videos, sus artistas y vistas
    for item in videos:
        # Verificar que el item tenga un videoId
        if 'videoId' in item['id']:
            titulo = item['snippet']['title']
            canal = item['snippet']['channelTitle']
            
            # Obtener el conteo de vistas
            vistas = None
            for estadistica in estadisticas:
                if estadistica['id'] == item['id']['videoId']:
                    vistas = estadistica['statistics'].get('viewCount', 'No disponible')
                    break
            
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

    # Guardar el archivo CSV
    df.to_csv(f'1videos_populares_{artista}.csv', index=False)

    print(f"Datos exportados a 1videos_populares_{artista}.csv")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
