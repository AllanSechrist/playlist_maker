from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import client_secrets


CLIENT_ID = client_secrets.id
CLIENT_SECRET = client_secrets.secret

scope = "playlist-modify-private"

auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com", scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)
id = sp.current_user()['id']


user_input = input("Which year would you like to travel to? The date must be in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{user_input}"
response = requests.get(URL)
top_100_page = response.text

soup = BeautifulSoup(top_100_page, "html.parser")

song_titles = [song.getText() for song in soup.find_all(name="span", class_="chart-element__information__song")]

year = user_input.split("-")[0]
song_list = []
for song in song_titles:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(user=id, name=f"{year} Billboard 100", public=False)
#print(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_list)


