Music Playlist Project

Обзор

Этот проект представляет собой музыкальный плейлист-менеджер на языке Python с использованием SQL для постоянного хранения данных. Он состоит из классов для управления треками, плейлистами и альбомами. Этот README предоставляет обзор структуры проекта, ключевых функций и инструкций по настройке и запуску проекта.

Структура проекта

	•	Track: Представляет один трек.
	•	Playlist: Управляет коллекцией треков.
	•	Album: Наследует от Playlist, обеспечивает, чтобы все треки принадлежали одному альбому и исполнителю.

Классы и методы

Класс Track

class Track:
    def __init__(self, id: int, name: str, album: str, artist: str, time: int):
        # Инициализация атрибутов трека

    def __str__(self):
        # Возвращает строковое представление трека

    def get_info(self):
        # Возвращает информацию о треке в виде словаря

    def save2db(self):
        # Сохраняет информацию о треке в базу данных

Класс Playlist

class Playlist:
    def __init__(self, tracks: list, name: str = '', author: str = ''):
        # Инициализация атрибутов плейлиста

    def append(self, track: Track):
        # Добавляет трек в плейлист

    def __str__(self):
        # Возвращает строковое представление плейлиста

    def remove_track(self, track: Track):
        # Удаляет трек из плейлиста

    def move2db(self):
        # Сохраняет информацию о плейлисте в базу данных

    @staticmethod
    def load_from_db(cls, playlist_id: int):
        # Загружает плейлист из базы данных

Класс Album

class Album(Playlist):
    def __init__(self, tracks: list, name: str = '', artist: str = ''):
        # Инициализация атрибутов альбома с проверкой

    def append(self, track: Track):
        # Добавляет трек в альбом с проверкой

    @classmethod
    def load_from_db(cls, playlist_id: int):
        # Загружает альбом из базы данных

Схема базы данных

Таблицы

	•	tracks: Хранит информацию о треках.
	•	playlists: Хранит информацию о плейлистах.
	•	playlist_tracks: Таблица связи между плейлистами и треками.

Пример схемы

CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    album TEXT,
    artist TEXT,
    time INTEGER
);

CREATE TABLE playlists (
    id INTEGER PRIMARY KEY,
    name TEXT,
    author TEXT
);

CREATE TABLE playlist_tracks (
    playlist_id INTEGER,
    track_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

Настройка и использование

Необходимые компоненты

	•	Python 3.x
	•	SQLite


python main.py



Пример main.py

def main():
    # Инициализация базы данных
    initialize_database()

    # Создание объектов треков для тестирования
    track1 = Track(1, "CORSO", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 141)
    track2 = Track(2, "LEMONHEAD", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 124)
    track3 = Track(3, "WUSYANAME", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 122)
    track4 = Track(4, "LUMBERJACK", "CALL ME IF YOU GET LOST", "Tyler, The Creator", 132)

    # Создание и сохранение альбома
    album = Album([track1, track2, track3, track4], "CALL ME IF YOU GET LOST", "Tyler, The Creator")
    album.save2db()

    # Загрузка альбома из базы данных
    loaded_album = Album.load_from_db(album.playlist_id)
    print("Загруженный альбом из базы данных:")
    print(loaded_album)

    # Дополнительное тестирование...

if __name__ == '__main__':
    main()
