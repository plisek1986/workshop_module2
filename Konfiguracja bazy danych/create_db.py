from psycopg2 import connect


CREATE_DB = 'CREATE DATABASE workshops_module2;'

USERS_TABLE = '''CREATE TABLE users (
            id serial not null,
            username varchar(255),
            hashed_password varchar(80),
            PRIMARY KEY(id)'''

MESSAGES_TABLE = '''CREATE TABLE messages (
            id serial not null,
            from_id int not null,
            to_id int not null,
            creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(id),
            FOREIGN KEY(from_id) REFERENCES users(id) ON DELETE  CASCADE,
            FOREIGN KEY(to_id) REFERENCES users(id) ON DELETE CASCADE)
             );'''

con = connect(user='postgres', password='coderslab', host='localhost', database='workshops_module2')
con.autocommit = True
cursor = con.cursor()
cursor.execute(CREATE_DB)

#
# def new_database(db_name):
#     cursor = con.cursor()
#     try:
#         cursor.execute('CREATE DATABASE %s', (db_name,))
#         db = cursor.fetchone()
#     raise DuplicateDatabase('The database already exists!')

