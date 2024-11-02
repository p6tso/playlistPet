import sqlite3


class Track:
    def __init__(self, id: int, name: str = 'no name', album: str = '', artist: str = 'unNoun', time: int = 0):
        self.id = id
        self.name = name
        self.album = album
        self.artist = artist
        self.time = time

    def __str__(self):
        result = self.name + ' - ' + self.artist + ' / ' + self.album + '\n'
        time = f'{self.time // 60}:{self.time % 60}'
        return result + time

    def get_info(self):
        return {'id': self.id, 'name': self.name, 'artist': self.artist, 'album': self.album, 'time': self.time}

    def save2db(self, db_name='music.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT OR REPLACE INTO tracks (id, name, album, artist, time) VALUES (?, ?, ?, ?, ?)',
                           (self.id, self.name, self.album, self.artist, self.time))
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
        finally:
            conn.close()
