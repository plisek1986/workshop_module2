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

#trying connection with the data base; before the db is created, Python should return
#OperationalError (connection error)
try:
    con = connect(user='postgres', password='coderslab', host='localhost', database='workshops_module2')
    con.autocommit = True
    cursor = con.cursor()
    #trying to create a database
    try:
        cursor.execute(CREATE_DB)
        print('The database has been created')
    except DuplicateDatabase as e:
        print('Data base already exists!', e)
    #trying to create a table for users and handling exception
    try:
        cursor.execute(USERS_TABLE)
        print('The table has been created')
    except DuplicateTable as e:
        print('Table already exists!', e)
    # trying to create a table for messages and handling exception
    try:
        cursor.execute(MESSAGES_TABLE)
        print('The table has been created')
    except DuplicateTable as e:
        print('Table already exists!', e)
        con.close()
# handling operational error
except OperationalError as e:
    print('Connection error', e)