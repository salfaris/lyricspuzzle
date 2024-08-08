from lyrics import find_song, save_song, Song

songs = [
    Song(artist="James Arthur", title="A Thousand Years"),
    Song(artist="James Arthur", title="Blindside"),
]

for song in songs:
    song = find_song(song)
    save_song(song)
