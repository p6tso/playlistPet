from playlist import Playlist
from track import Track
from typing import List
import sqlite3


class Album(Playlist):
    def __init__(self, tracks: List[Track], name: str = '', artist: str = '', playlist_id: int = None):
        super().__init__(tracks, name, artist, playlist_id)
        for track in tracks:
            info = track.get_info()
            if info['album'] != self.name or info['artist'] != self.author:
                raise ValueError(f'Incorrect track: {info["name"]}. '
                                 f'Expected album: {self.name}, artist: {self.author}.')

    def append(self, track: Track):
        info = track.get_info()
        if info['album'] != self.name:
            raise ValueError(f'Incorrect track: {info["name"]}. '
                             f'Expected album: {self.name}.')
        if info['artist'] != self.author:
            raise ValueError(f'Incorrect track: {info["name"]}. '
                             f'Expected artist: {self.author}.')
        super().append(track)

    @classmethod
    def load_from_db(cls, playlist_id: int, db_name="music.db"):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT name, author FROM playlists WHERE id = ?', (playlist_id,))
        row = cursor.fetchone()
        if row:
            name, author = row
        else:
            raise ValueError(f"Playlist with id {playlist_id} not found.")

        cursor.execute('''SELECT t.id, t.name, t.album, t.artist, t.time
                              FROM tracks t
                              JOIN playlist_tracks pt ON t.id = pt.track_id
                              WHERE pt.playlist_id = ?''', (playlist_id,))
        tracks_data = cursor.fetchall()

        tracks = []
        for track_data in tracks_data:
            track_id, track_name, album_name, artist_name, time = track_data
            track = Track(track_id, track_name, album_name, artist_name, time)
            tracks.append(track)

        conn.close()

        album = cls(tracks, name, author)
        return album
