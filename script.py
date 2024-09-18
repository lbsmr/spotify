import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
import os

# Autenticación en Spotify
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Configurar credenciales
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Cargar el archivo CSV
df = pd.read_csv('spotify-2023.csv',encoding="ISO-8859-1")

# Agregar columna para las URLs de las portadas
df['Album_Cover_URL'] = None

# Función para obtener la URL de la portada de Spotify
def get_album_cover_url(song_name, artist_name):
    result = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
    if result['tracks']['items']:
        return result['tracks']['items'][0]['album']['images'][0]['url']
    else:
        return None

# Iterar sobre el DataFrame y buscar las portadas
for idx, row in df.iterrows():
    song = row['track_name']  # Asumiendo que la columna del nombre de la canción se llama 'track_name'
    artist = row['artist(s)_name']  # Asumiendo que la columna del artista se llama 'artist(s)_name'
    cover_url = get_album_cover_url(song, artist)
    df.at[idx, 'Album_Cover_URL'] = cover_url

# Guardar el nuevo archivo CSV con la columna de URLs de las portadas
df.to_csv('spotify_2023_with_covers.csv', index=False)

print("Archivo CSV actualizado con las URLs de las portadas.")