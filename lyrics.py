from getpass import getpass
import os
from pathlib import Path
import shutil

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


def find_song(song: Song) -> lyricsgenius.types.Song:
    song = GENIUS.search_song(song.title, song.artist)
    return song


def save_song(song: lyricsgenius.types.Song):
    fname = "{}_{}".format(
        _to_camel_case(song.artist),
        _to_camel_case(song.title),
    )
    ext = "txt"
    song.save_lyrics(filename=fname, extension=ext)

    fname_ext = f"{fname}.{ext}"

    shutil.move(fname_ext, LYRICS_LIB / fname_ext)
