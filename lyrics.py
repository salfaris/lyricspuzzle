from getpass import getpass
import os
from pathlib import Path
import shutil

from lyricsgenius import Genius
from lyricsgenius.types import Song

LYRICS_LIB = Path(__file__) / "lyrics"
LYRICS_LIB.mkdir(exist_ok=True, parents=True)

try:
    access_token = os.environ["GENIUS_ACCESS_TOKEN"]
except KeyError:
    print("Cannot find GENIUS_ACCESS_TOKEN in environ...")
    access_token = getpass()

GENIUS = Genius(access_token=access_token)


def _lyrics_fname_fmt(s):
    return "_".join(s.lower().split(" "))


def find_song(title: str, artist_name: str):
    song = GENIUS.search_song(title, artist_name)
    return song


def save_song(song: Song):
    fname = "{}_{}".format(
        _lyrics_fname_fmt(song.artist),
        _lyrics_fname_fmt(song.title),
    )
    ext = "txt"
    song.save_lyrics(filename=fname, extension=ext)

    fname_ext = f"{fname}.{ext}"

    shutil.move(fname_ext, LYRICS_LIB / fname_ext)
