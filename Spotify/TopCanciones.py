import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Coloca aquí tus credenciales de la API de Spotify
client_id = '032d057c494e430ea6855d3c84cbd342'
client_secret = 'f8f7fca76651497c9f5853d7c1ab39ec'

# Autenticación con Spotify usando las credenciales
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ID de la playlist 'Top 50 Global' en Spotify
playlist_id = '37i9dQZEVXbMDoHDwVN2tF'

# Función para obtener las canciones más populares de la playlist 'Top 50 Global' con el género del artista
def obtener_top_50_canciones_con_genero():
    # Obtener las pistas de la playlist
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=50)  # Limitar a las 50 primeras canciones
    
    # Lista para almacenar la información de las canciones
    data_canciones = []
    
    print("Canciones más populares en la playlist 'Top 50 Global':\n")
    
    for idx, item in enumerate(playlist_tracks['items']):
        track = item['track']
        nombre_cancion = track['name']
        artistas = ', '.join([artist['name'] for artist in track['artists']])
        artista_id = track['artists'][0]['id']  # Tomamos el ID del primer artista (puedes tomar todos si lo deseas)
        album = track['album']['name']
        url_cancion = track['external_urls']['spotify']
        popularidad = track['popularity']
        
        # Obtener el género del artista
        artista_info = sp.artist(artista_id)  # Consultar el artista por ID
        generos = ', '.join(artista_info['genres']) if artista_info['genres'] else 'Desconocido'
        
        # Mostrar la información de la canción
        print(f"{idx+1}. {nombre_cancion} - {artistas}")
        print(f"   Álbum: {album}")
        print(f"   Popularidad: {popularidad}")
        print(f"   Géneros: {generos}")
        print(f"   URL de Spotify: {url_cancion}\n")
        
        # Guardar la información de la canción en un diccionario
        cancion_info = {
            'Posición': idx + 1,
            'Nombre de la canción': nombre_cancion,
            'Artistas': artistas,
            'Álbum': album,
            'Popularidad': popularidad,
            'Géneros del artista': generos,
            'URL de Spotify': url_cancion
        }
        
        # Añadir la información de la canción a la lista
        data_canciones.append(cancion_info)
    
    # Crear un DataFrame con la información de las canciones
    df = pd.DataFrame(data_canciones)

    # Guardar el DataFrame en un archivo CSV que puede abrirse con Excel
    df.to_csv('top_50_canciones_con_genero_spotify.csv', index=False)

    print("\nLa información de las canciones se ha guardado en 'top_50_canciones_con_genero_spotify.csv'.")

# Llamar a la función para obtener el Top 50 de canciones con el género del artista
obtener_top_50_canciones_con_genero()