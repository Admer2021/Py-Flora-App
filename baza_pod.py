import sqlite3
def inicijalizacija():
    global database_name
    query_create =(''' CREATE TABLE IF NOT EXISTS Tablica_korisnici (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password INTEGER,
                    email TEXT NOT NULL
                    )''')

    query_create_biljke =(''' CREATE TABLE IF NOT EXISTS Tablica_biljke (
                    id INTEGER PRIMARY KEY,
                    naziv TEXT ,
                    slika BLOB,
                    njega TEXT 
                    )''')
    
    query_create_posuda = ('''CREATE TABLE IF NOT EXISTS Tablica_posude (
        posuda_id INTEGER PRIMARY KEY,
        biljka_id TEXT,
        FOREIGN KEY (biljka_id) REFERENCES Tablica_biljke (naziv)
    )''')

    query_create_prognoza = ('''CREATE TABLE IF NOT EXISTS Tablica_prognoza (
        id INTEGER PRIMARY KEY,
        naziv TEXT,
        slika TEXT
    )''')

    database_name= "Korisnici.db"

    try: 
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute(query_create)
        cursor.execute(query_create_biljke)
        cursor.execute(query_create_posuda)
        cursor.execute(query_create_prognoza)
        connection.commit()               

        cursor.close()

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri spajanju na SQLite bazu {e}")

    finally:
        if connection:
            connection.close()

inicijalizacija()