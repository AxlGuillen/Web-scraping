from googleapiclient.discovery import build
import pandas as pd
import unidecode

# Clave de API (reemplaza con tu propia API key)
api_key = 'AIzaSyB14E76hfuE1ymxgqxkGv8wxPudF4M-4GM'

# Función para obtener comentarios de un video
def obtener_comentarios(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comentarios = []
    
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Número de comentarios a obtener
    )
    response = request.execute()
    
    for item in response['items']:
        comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
        autor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comentarios.append({
            'Autor': unidecode.unidecode(autor),
            'Comentario': unidecode.unidecode(comentario)
        })
    
    return comentarios

# Función principal
def main():
    video_id = input("Ingresa el ID del video: ")
    
    # Obtener comentarios del video
    comentarios = obtener_comentarios(video_id)

    # Crear un DataFrame de pandas
    df = pd.DataFrame(comentarios)

    # Guardar el archivo CSV
    df.to_csv(f'1comentarios_video_{video_id}.csv', index=False)

    print(f"Datos de comentarios exportados a comentarios_video_{video_id}.csv")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
