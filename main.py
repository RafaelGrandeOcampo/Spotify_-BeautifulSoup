import export as export
import requests
from bs4 import BeautifulSoup


#fecha = input('Introduce una fecha(YYY-MM-DD): ')
fecha = '2000-01-01'
year = '2000'


response = requests.get(f'https://www.billboard.com/charts/hot-100/2000-01-01/')
data = response.text
soup = BeautifulSoup(data, 'html.parser')

song = soup.find_all(name='h3', class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

lista_canciones = [title.getText().strip() for title in song]

print(lista_canciones)

############## crear lista en spotify


import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-private"

SPOTIPY_CLIENT_ID= '3ee902aa633f485bbaf144969422c2fb'
SPOTIPY_CLIENT_SECRET= '69f2542defcb443c848ddf61dc4a94c5'
SPOTIPY_REDIRECT_URI= 'http://example.com'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope, show_dialog=True, cache_path=".cache"))

uri_listado_canciones = []

for song in lista_canciones:

    resultado = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = resultado["tracks"]["items"][0]["uri"]
        uri_listado_canciones.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



id = sp.current_user()['id']


create_playlist = sp.user_playlist_create(user=id, name=f'{fecha} Billboard 100', public=False)
print(create_playlist)

sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_listado_canciones)