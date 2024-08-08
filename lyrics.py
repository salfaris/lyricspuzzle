from getpass import getpass
import os
from pathlib import Path
import shutil
import unicodedata

import lyricsgenius
from lyricsgenius import Genius
from pydantic import BaseModel


class Song(BaseModel):
    artist: str
    title: str


LYRICS_LIB = Path(__file__).parents[0] / "lyrics"
LYRICS_LIB.mkdir(exist_ok=True, parents=True)

try:
    access_token = os.environ["GENIUS_ACCESS_TOKEN"]
except KeyError:
    print("Cannot find GENIUS_ACCESS_TOKEN in environ...")
    access_token = getpass()

GENIUS = Genius(access_token=access_token)


def _to_camel_case(text):
    words = text.split()
    camel_case_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    camel_case_text = "".join(camel_case_words)
    return camel_case_text


def _preprocess(text: str):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lstrip()
    return text


def find_song(song: Song) -> lyricsgenius.types.Song:
    song = GENIUS.search_song(song.title, song.artist)
    return song


def save_song(song: lyricsgenius.types.Song):
    artist = _preprocess(song.artist)
    title = _preprocess(song.title)

    fname = "{}_{}".format(_to_camel_case(artist), _to_camel_case(title))
    ext = "txt"
    song.save_lyrics(filename=fname, extension=ext, overwrite=True)

    def add_artist_title_top(filename):
        with open(filename, "r+") as f:
            content = f.read()

            # Insert the new line at the beginning of the file
            f.seek(0)
            f.write(f"{artist} - {title}\n\n" + content)

    fname_ext = f"{fname}.{ext}"
    add_artist_title_top(fname_ext)

    shutil.move(fname_ext, LYRICS_LIB / fname_ext)
