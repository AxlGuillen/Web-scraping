import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Credenciales
client_id = '032d057c494e430ea6855d3c84cbd342'
client_secret = 'f8f7fca76651497c9f5853d7c1ab39ec'

# Autenticación con Spotify usando las credenciales
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Lista para almacenar los datos
data_artistas = []

# Función para obtener las canciones más populares de un artista
def obtener_canciones_populares_de_artista(artista_id):
    top_tracks = sp.artist_top_tracks(artista_id)
    canciones = []
    
    for idx, track in enumerate(top_tracks['tracks'][:10]):  # Limitar a 10 canciones
        nombre_cancion = track['name']
        popularidad = track['popularity']
        album = track['album']['name']
        url_cancion = track['external_urls']['spotify']
        
        # Formatear la información de la canción
        canciones.append(f"{idx+1}. {nombre_cancion} (Popularidad: {popularidad}) - Álbum: {album} - {url_cancion}")
    
    return canciones

# Función para obtener los álbumes más recientes de un artista
def obtener_albumes_recientes_de_artista(artista_id):
    albums = sp.artist_albums(artista_id, album_type='album', limit=5)  # Limitar a los 5 álbumes más recientes
    albumes = []
    
    for album in albums['items']:
        nombre_album = album['name']
        fecha_lanzamiento = album['release_date']
        url_album = album['external_urls']['spotify']
        
        # Formatear la información del álbum
        albumes.append(f"{nombre_album} (Lanzamiento: {fecha_lanzamiento}) - {url_album}")
    
    return albumes

# Función para obtener información del artista, sus canciones y álbumes
def obtener_info_artista(nombre_artista):
    resultado = sp.search(q=nombre_artista, type='artist', limit=1)
    
    if resultado['artists']['items']:
        artista = resultado['artists']['items'][0]
        
        # Información del artista
        nombre = artista['name']
        popularidad = artista['popularity']
        seguidores = artista['followers']['total']
        generos = ', '.join(artista['genres'])
        url_spotify = artista['external_urls']['spotify']
        imagen = artista['images'][0]['url'] if artista['images'] else 'No disponible'
        
        # Obtener las 10 canciones más populares del artista
        canciones_populares = obtener_canciones_populares_de_artista(artista['id'])
        canciones_populares_str = '\n'.join(canciones_populares)  # Convertir la lista de canciones a un solo string
        
        # Obtener los 5 álbumes más recientes del artista
        albumes_recientes = obtener_albumes_recientes_de_artista(artista['id'])
        albumes_recientes_str = '\n'.join(albumes_recientes)  # Convertir la lista de álbumes a un solo string
        
        # Guardar la información en un diccionario
        artista_info = {
            'Nombre del artista': nombre,
            'Popularidad': popularidad,
            'Seguidores': seguidores,
            'Géneros': generos,
            'URL de Spotify': url_spotify,
            'Imagen': imagen,
            'Canciones populares': canciones_populares_str,
            'Álbumes recientes': albumes_recientes_str
        }
        
        # Añadir la información del artista a la lista
        data_artistas.append(artista_info)

# Función para obtener el top de artistas
def obtener_top_artistas(limit=10):
    # Búsqueda de artistas en el género 'pop' (puedes cambiar el género)
    resultado = sp.search(q='genre:pop', type='artist', limit=limit)
    
    print(f"Top {limit} artistas populares en Spotify:\n")
    for idx, artista in enumerate(resultado['artists']['items']):
        print(f"{idx+1}. {artista['name']}")
        obtener_info_artista(artista['name'])

    # Crear un DataFrame con la información de los artistas
    df = pd.DataFrame(data_artistas)

    # Guardar el DataFrame en un archivo CSV que puede abrirse con Excel
    df.to_csv('top_artistas_spotify.csv', index=False)

    print("\nLa información se ha guardado en 'top_artistas_spotify.csv'.")

# Obtener el top 50 de artistas y guardar la información en un archivo CSV
obtener_top_artistas(50)