from track import Track
from typing import List
import sqlite3


class Playlist:

    def __init__(self, tracks: list, name: str = '', author: str = '', playlist_id: int = None):
        for track in tracks:
            assert isinstance(track, Track), 'invalid type of tracks'
        self.trackHolder = tracks
        self.name = name
        self.author = author
        self.playlist_id = playlist_id

    def append(self, track: Track):
        if not isinstance(track, Track):
            raise TypeError('track must be an instance of Track.')
        self.trackHolder.append(track)

    def __str__(self):
        result = f'{self.name} by {self.author}'
        for track in self.trackHolder:
            result += f'\n-----\n{track}'
        return result

    def remove_track(self, track: Track):
        if track not in self.trackHolder:
            raise ValueError('track not found in the playlist.')
        self.trackHolder.remove(track)
        return track

    def save2db(self, db_name='music.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS playlists
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, author TEXT)''')
        if self.playlist_id is None:
            cursor.execute('INSERT INTO playlists (name, author) VALUES (?, ?)', (self.name, self.author))
            self.playlist_id = cursor.lastrowid
        else:
            cursor.execute('UPDATE playlists SET name = ?, author = ? WHERE id = ?',
                           (self.name, self.author, self.playlist_id))

        cursor.execute('''CREATE TABLE IF NOT EXISTS playlist_tracks
                          (playlist_id INTEGER, track_id INTEGER,
                           FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                           FOREIGN KEY (track_id) REFERENCES tracks(id))''')

        conn.commit()
        conn.close()
        for track in self.trackHolder:
            track.save2db(db_name)
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute('INSERT OR REPLACE INTO playlist_tracks (playlist_id, track_id) VALUES (?, ?)',
                           (self.playlist_id, track.id))
            conn.commit()
            conn.close()

    @staticmethod
    def load_from_db(playlist_id, db_name='music.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT name, author FROM playlists WHERE id = ?', (playlist_id,))
        playlist_data = cursor.fetchone()
        name, author = playlist_data if playlist_data else ('', '')

        cursor.execute('SELECT track_id FROM playlist_tracks WHERE playlist_id = ?', (playlist_id,))
        track_ids = cursor.fetchall()

        tracks = []
        for (track_id,) in track_ids:
            cursor.execute('SELECT id, name, album, artist, time FROM tracks WHERE id = ?', (track_id,))
            track_data = cursor.fetchone()
            if track_data:
                tracks.append(Track(*track_data))

        conn.close()
        return Playlist(tracks, name, author, playlist_id)

    def delete_from_db(self, db_name='music.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM playlists WHERE name = ? AND author = ?', (self.name, self.author))
        playlist_id = cursor.fetchone()[0]

        cursor.execute('DELETE FROM playlist_tracks WHERE playlist_id = ?', (playlist_id,))
        cursor.execute('DELETE FROM playlists WHERE id = ?', (playlist_id,))

        conn.commit()
        conn.close()
