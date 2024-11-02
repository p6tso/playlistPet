from track import Track
from playlist import Playlist
from album import Album
import sqlite3


def initialize_database(db_name='music.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tracks
                      (id INTEGER PRIMARY KEY, name TEXT, album TEXT, artist TEXT, time INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS playlists
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, author TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS playlist_tracks
                      (playlist_id INTEGER, track_id INTEGER,
                       FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                       FOREIGN KEY (track_id) REFERENCES tracks(id))''')

    conn.commit()
    conn.close()


def main():
    initialize_database()

    track1 = Track(1, "CORSO", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 141)
    track2 = Track(2, "LEMONHEAD", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 124)
    track3 = Track(3, "WUSYANAME", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 122)
    track4 = Track(4, "LUMBERJACK", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 132)
    track5 = Track(5, "HOT WIND BLOWS", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 161)
    track6 = Track(6, "TRACK 6", "ALBUM 2", "Artist 2", 150)
    track7 = Track(7, "TRACK 7", "ALBUM 2", "Artist 2", 200)

    album = Album([track1, track2, track3, track4, track5], "CALL ME IF YOU GET LOST", "Tyler, The Creator")
    album.save2db()
    loaded_album = Album.load_from_db(album.playlist_id)
    print("Loaded Album from DB:")
    print(loaded_album)
    try:
        loaded_album.append(track7)
    finally:
        print("works correctly")
    print(loaded_album)

    playlist = Playlist([track1, track6, track7], "My Mixed Playlist", "Various Artists")
    playlist.save2db()
    loaded_playlist = Playlist.load_from_db(playlist.playlist_id)
    print("Loaded Playlist from DB:")
    print(loaded_playlist)

    removed_track = playlist.remove_track(track6)
    print(f"Removed Track: {removed_track}")
    playlist.save2db()

    updated_playlist = Playlist.load_from_db(playlist.playlist_id)
    print("Updated Playlist from DB:")
    print(updated_playlist)

    playlist.append(track5)
    playlist.save2db()
    reloaded_playlist = Playlist.load_from_db(playlist.playlist_id)
    print("Reloaded Playlist after adding a track:")
    print(reloaded_playlist)

    playlist.remove_track(track5)
    playlist.save2db()
    final_playlist = Playlist.load_from_db(playlist.playlist_id)
    print("Final Playlist after removing the added track:")
    print(final_playlist)

    playlist2 = Playlist([track2, track3, track4], "Another Playlist", "Various Artists")
    playlist2.save2db()
    loaded_playlist2 = Playlist.load_from_db(playlist2.playlist_id)
    print("Loaded Second Playlist from DB:")
    print(loaded_playlist2)

    album2 = Album([track6, track7], "ALBUM 2", "Artist 2")
    album2.save2db()
    loaded_album2 = Playlist.load_from_db(album2.playlist_id)
    print("Loaded Second Album from DB:")
    print(loaded_album2)

    playlist3 = Playlist([track1, track2, track3, track4, track5, track6, track7], "Complete Playlist",
                         "Various Artists")
    playlist3.save2db()
    loaded_playlist3 = Playlist.load_from_db(playlist3.playlist_id)
    print("Loaded Complete Playlist from DB:")
    print(loaded_playlist3)


if __name__ == "__main__":
    main()
