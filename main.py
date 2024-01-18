import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

# Solicitar al usuario la fecha o utilizar una predefinida
fecha = input('Introduce una fecha (YYYY-MM-DD): ')
fecha = '2000-01-01'
year = fecha[0:4]

# Obtener las canciones de Billboard para la fecha especificada
response = requests.get(f'https://www.billboard.com/charts/hot-100/{fecha}/')
if response.status_code == 200:
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    # Obtener las canciones del sitio de Billboard
    canciones_html = soup.find_all(name='h3', class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
    
    # Crear una lista de nombres de canciones
    lista_canciones = [cancion.getText().strip() for cancion in canciones_html]

    print(f'Lista de canciones de Billboard el {fecha}:')
    print(lista_canciones)
else:
    print(f"Error al obtener la página de Billboard. Código de estado: {response.status_code}")

# Configuración de la autenticación de Spotify
scope = "playlist-modify-private"
SPOTIPY_CLIENT_ID = '[ID_CLiente]'
SPOTIPY_CLIENT_SECRET = '[Secret_Key]'
SPOTIPY_REDIRECT_URI = 'http://example.com'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope, show_dialog=True, cache_path=".cache"))

# Crear una lista de URIs de las canciones
uri_listado_canciones = []

for cancion in lista_canciones:
    resultado = sp.search(q=f"track:{cancion} year:{year}", type="track")
    try:
        uri = resultado["tracks"]["items"][0]["uri"]
        uri_listado_canciones.append(uri)
    except IndexError:
        print(f"Advertencia: {cancion} no existe en Spotify. Se ha omitido.")

# Obtener el ID del usuario actual en Spotify
id_usuario_spotify = sp.current_user()['id']

# Crear una nueva lista de reproducción en Spotify
crear_lista_reproduccion = sp.user_playlist_create(user=id_usuario_spotify, name=f'{fecha} Billboard 100', public=False)
print(crear_lista_reproduccion)

# Agregar canciones a la lista de reproducción en Spotify
sp.playlist_add_items(playlist_id=crear_lista_reproduccion['id'], items=uri_listado_canciones)
