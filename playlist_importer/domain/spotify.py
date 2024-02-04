class Song:
    title: str
    album: str
    artist: str

    def __init__(self, title, album, artist):
        self.title = title
        self.album = album
        self.artist = artist

    def __str__(self):
        return f"(t={self.title},al={self.album},ar={self.artist})"

    def __repr__(self):
        return f"(t={self.title},al={self.album},ar={self.artist})"


class Playlist:
    name: str
    songs: list[Song]

    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

    def __str__(self):
        return f"{self.name} = {self.songs}"

    def __repr__(self):
        return f"{self.name} = {self.songs}"
