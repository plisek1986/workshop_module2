from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable



CREATE_DB = 'CREATE DATABASE workshops_module2;'

USERS_TABLE = '''CREATE TABLE users (
            id serial not null,
            username varchar(255),
            hashed_password varchar(80),
            PRIMARY KEY(id)
            );'''

MESSAGES_TABLE = '''CREATE TABLE messages (
            id serial not null,
            from_id int not null,
            to_id int not null,
            creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id),
            FOREIGN KEY(from_id) REFERENCES users(id) ON DELETE  CASCADE,
            FOREIGN KEY(to_id) REFERENCES users(id) ON DELETE CASCADE
             );'''


try:
    con = connect(user='postgres', password='coderslab', host='localhost', database='workshops_module2')
    con.autocommit = True
    cursor = con.cursor()
    try:
        cursor.execute(CREATE_DB)
        print('The database has been created')
    except DuplicateDatabase as e:
        print('Data base already exists!', e)
    try:
        cursor.execute(USERS_TABLE)
        print('The table has been created')
    except DuplicateTable as e:
        print('Table already exists!', e)
    try:
        cursor.execute(MESSAGES_TABLE)
        print('The table has been created')
    except DuplicateTable as e:
        print('Table already exists!', e)
        con.close()
except OperationalError as e:
    print('Connection error', e)