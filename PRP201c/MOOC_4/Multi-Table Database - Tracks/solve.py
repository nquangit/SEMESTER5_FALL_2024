
import sqlite3

#Function that we'll use to find the content of a specific field.
def find_field(track, wanted_field):
    """This function gets two parameters: track, a list of a record , and wanted_field, a string representing the
    title of the tag we want to obtain.
    It works by finding a key tag with the text {wanted_field}, and
    returning the content of the following tag. If wanted_field doesn't
    match any tag, it returns a False"""

    headers = ["Name", "Artist", "Genre", "Album", "Total Time", "Play Count", "Rating"]

    #We'll get the index of the wanted_field
    try:
        index = headers.index(wanted_field)
    except ValueError:
        return False
    
    #We'll get the content of the field
    field = track.split(",")[index]
    return field


#PART 1: PREPARING THE DATABASE
#Connecting to the file in which we want to store our db
conn = sqlite3.connect('tracks.sqlite')
cur = conn.cursor()

#Getting sure it is empty
#We can use "executescript" to execute several statements at the same time
cur.executescript("""
    DROP TABLE IF EXISTS Artist;

    DROP TABLE IF EXISTS Album; 
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Track
    """)

#Creating it
cur.executescript(''' CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


#PART 2: INSERTING THE DATA
#Getting the data and parsing it
data_source = open("tracks/tracks.csv")
data = data_source.readlines()


tracks_data = data

#Getting the values of the fields we'll insert
for track in tracks_data:
    title = find_field(track, "Name")
    artist = find_field(track, "Artist")
    genre = find_field(track, "Genre")
    album = find_field(track, "Album")
    length = find_field(track, "Total Time")
    count = find_field(track, "Play Count")
    rating = find_field(track, "Rating")

    #Artist
    if (artist): #If it's a filled string, != False
        #If the value hasn't been introduced yet and exists, we'll insert it
        artist_statement = """INSERT INTO Artist(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Artist WHERE name = ?)"""
        SQLparams = (artist, artist) #Params needed for completing the statement
        cur.execute(artist_statement, SQLparams)

    #Genre
    if (genre): #If it's a filled string, != False
        #If the value hasn't been introduced yet and exists, we'll insert it
        genre_statement = """INSERT INTO Genre(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Genre WHERE name = ?)"""
        SQLparams = (genre, genre)
        cur.execute(genre_statement, SQLparams)

    #Album
    if (album): #If it's a filled string, != False
        #First of all, we'll get the artist id
        artistID_statement = "SELECT id from Artist WHERE name = ?"
        cur.execute(artistID_statement, (artist, ))
        #.fetchone() returns a one-element tuple, and we want its content
        artist_id = cur.fetchone()[0]


        #Now we're going to insert the data
        album_statement = """INSERT INTO Album(title, artist_id) 
            SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Album WHERE title = ?)"""
        SQLparams = (album, artist_id, album)
        cur.execute(album_statement, SQLparams)

    #Track
    if (title): #If it's a filled string, != False
        #Obtaining genre_id
        genreID_statement = "SELECT id from Genre WHERE name = ?"
        cur.execute(genreID_statement, (genre, ))
        try:
            genre_id = cur.fetchone()[0]
        except TypeError:
            genre_id = 0
        #Obtaining album_id
        albumID_statement = "SELECT id from Album WHERE title = ?"
        cur.execute(albumID_statement, (album, ))
        try:
            album_id = cur.fetchone()[0]
        except TypeError:
            album_id = 0

        #Inserting data
        track_statement = """INSERT INTO Track(title, album_id, genre_id, len,
            rating, count) SELECT ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT * FROM Track WHERE title = ?)"""
        SQLparams = (title, album_id, genre_id, length, rating, count, title)
        cur.execute(track_statement, SQLparams)


conn.commit()
cur.close()