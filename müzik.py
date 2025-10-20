import streamlit as st
import pandas as pd
import datetime
import random
import csv
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API kimlik bilgileri
SPOTIFY_CLIENT_ID = "6d73f541909e4de2bd08a7971e516bdc"
SPOTIFY_CLIENT_SECRET = "723a7b5bb24a4196954c93096a6de54f"

# Spotify bağlantısı
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Kullanıcı girişi
st.set_page_config(page_title="Ruh Haline Göre Müzik", page_icon="🎵")
st.title("🎵 Ruh Haline Göre Müzik Önerisi + Spotify + Günlük + Giriş")

username = st.text_input("👤 Kullanıcı adınızı girin:")
if not username:
    st.warning("Devam etmek için kullanıcı adınızı girin.")
    st.stop()

# Kullanıcıya özel dosya
def get_user_file():
    return f"{username}_songs.csv"

# Şarkı kaydetme
def save_custom_song(track, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["mood", "artist", "song", "url", "origin"])
        writer.writerow([track["mood"], track["artist"], track["song"], track["url"], track["origin"]])

# Şarkı okuma
def load_custom_songs(filename):
    if not os.path.isfile(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# Spotify'dan şarkı arama
def search_spotify_link(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    results = sp.search(q=query, type="track", limit=1)
    if results["tracks"]["items"]:
        return results["tracks"]["items"][0]["external_urls"]["spotify"]
    return ""

# Sabit müzik verisi (örnek)
music_data = {
    "Mutlu": {
        "yerli": [
            {"artist": "Sezen Aksu", "song": "Gülümse", "url": search_spotify_link("Gülümse", "Sezen Aksu")},
            {"artist": "MFÖ", "song": "Güllerin İçinden", "url": search_spotify_link("Güllerin İçinden", "MFÖ")}
        ],
        "yabancı": [
            {"artist": "Pharrell Williams", "song": "Happy", "url": search_spotify_link("Happy", "Pharrell Williams")},
            {"artist": "Bruno Mars", "song": "Uptown Funk", "url": search_spotify_link("Uptown Funk", "Bruno Mars")}
        ]
    }
}

# Ruh hali seçimi
selected_mood = st.selectbox("Bugünkü ruh halin nedir?", list(music_data.keys()))

# Ruh hali günlüğü
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

# Şarkı önerisi
if st.button("🎧 Şarkı Öner!"):
    yerli_sabit = music_data[selected_mood]["yerli"]
    yabancı_sabit = music_data[selected_mood]["yabancı"]

    custom_songs = load_custom_songs(get_user_file())
    yerli_custom = [s for s in custom_songs if s["mood"] == selected_mood and s.get("origin") == "yerli"]
    yabancı_custom = [s for s in custom_songs if s["mood"] == selected_mood and s.get("origin") == "yabancı"]

    yerli_all = yerli_sabit + yerli_custom
    yabancı_all = yabancı_sabit + yabancı_custom

    yerli_final = random.sample(yerli_all, min(5, len(yerli_all)))
    yabancı_final = random.sample(yabancı_all, min(5, len(yabancı_all)))

    st.subheader("🇹🇷 Yerli Şarkılar")
    for track in yerli_final:
        st.markdown(f"**{track['song']}** – {track['artist']}")
        if track.get("url"):
            st.markdown(f"[Spotify'da Dinle]({track['url']})")

    st.subheader("🌍 Yabancı Şarkılar")
    for track in yabancı_final:
        st.markdown(f"**{track['song']}** – {track['artist']}")
        if track.get("url"):
            st.markdown(f"[Spotify'da Dinle]({track['url']})")

    st.session_state.mood_log.append({"date": datetime.date.today(), "mood": selected_mood})

# Ruh hali günlüğü grafiği
st.subheader("📊 Ruh Hali Günlüğü")
if st.session_state.mood_log:
    df = pd.DataFrame(st.session_state.mood_log)
    mood_counts = df["mood"].value_counts()
    st.bar_chart(mood_counts)
    st.dataframe(df)

# Şarkı ekleme formu
st.subheader("🎵 Kendi Şarkını Ekle")
with st.form("custom_song_form"):
    mood_input = st.selectbox("Şarkının ruh hali:", list(music_data.keys()))
    artist_input = st.text_input("Sanatçı adı")
    song_input = st.text_input("Şarkı adı")
    origin_input = st.radio("Yerli mi yabancı mı?", ["yerli", "yabancı"])
    submitted = st.form_submit_button("Ekle")

    if submitted and artist_input and song_input:
        url = search_spotify_link(song_input, artist_input)
        new_track = {
            "mood": mood_input,
            "artist": artist_input,
            "song": song_input,
            "url": url,
            "origin": origin_input
        }
        save_custom_song(new_track, get_user_file())
        st.success("Şarkı başarıyla eklendi!")

# Eklenen şarkılar listesi
custom_songs = load_custom_songs(get_user_file())
if custom_songs:
    st.subheader("🎶 Eklediğin Şarkılar")
    for track in custom_songs:
        origin = track.get("origin", "bilinmiyor")
        st.markdown(f"**{track['song']}** – {track['artist']} ({track['mood']}, {origin})")
        if track.get("url"):
            st.markdown(f"[Spotify'da Dinle]({track['url']})")
