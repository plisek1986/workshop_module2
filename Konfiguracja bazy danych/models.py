from clcrypto import hash_password
from psycopg2 import connect


class User:
    """
    This class defines actions for user and password management
    """
    # define the connection with database
    con = connect(user='postgres', host='localhost', password='coderslab',
                  database='workshops_module2')
    con.autocommit = True
    cursor = con.cursor()

    # define init method
    def __init__(self, username='', hashed_password=''):
        self._id = -1
        self.username = username
        self._hashed_password = hashed_password

    # define dynamic properties for sensitive data
    @property
    def id(self):
        return self._id

    # define dynamic properties for sensitive data
    @property
    def hashed_password(self):
        return self._hashed_password

    # we need this function because in the end we want to store
    # only the hashed value of the password
    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    # define setter for dynamic property of password
    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    # define method for saving a new user to the database
    def save_to_db(self, cursor):
        if self._id == -1:
            cursor.execute('''INSERT INTO users (username, hashed_password) VALUES (%s, %s)
                           RETURNING id''', (self.username, self.hashed_password))
            self._id = cursor.fetchone()[0]
        else:
            cursor.execute('UPDATE users SET username=%s, hashed_password=%s WHERE id=%s',
                           (self.username, self.hashed_password, self.id))
            cursor.fetchone()
            return True

    # define a static method for loading a user from the
    # database using his/her username as an atribute
    @staticmethod
    def load_user_by_username(cursor, username):
        cursor.execute('SELECT id, username, hashed_password FROM users where username=%s',
                       (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._password = hashed_password
            return loaded_user
        return None

    # define a static method for loading a user from the
    # database using his/her id as an atribute
    @staticmethod
    def load_user_by_id(cursor, id_):
        cursor.execute('SELECT id, username, hashed_password FROM users where username=%s',
                       (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        return None

    # define a static method for loading all users from the database
    @staticmethod
    def load_all_users(cursor):
        users = []
        cursor.execute('SELECT id, username, hashed_password FROM users')
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    # define a method for deleting users from the database = THIS IS NOT A STATIC METHOD!!
    def delete(self, cursor):
        cursor.execute('DELETE * FROM users WHERE id=%s', (self.id,))
        self._id = -1
        return True


class Messages:

    con = connect(user='postgres', host='localhost', password='coderslab',
                  database='workshops_module2')
    con.autocommit = True
    cursor = con.cursor()

    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_data = None

    @property
    def creation_data(self):
        return self._creation_data

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            cursor.execute('''INSERT INTO messages (from_id, to_id, text) VALUES (%s, %s, %s)
                           RETURNING id''', (self.from_id, self.to_id, self.text))
            self._id = cursor.fetchone()[0]
        else:
            cursor.execute('UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s',
                           (self.from_id, self.to_id, self.text, self.id))
            cursor.fetchone()
            return True
        return False

    @staticmethod
    #we add the optional parameter user_id so that if it is provided, we can filter for messages for this
    #concrete user_id
    def load_all_messages(cursor, user_id=None):
        messages = []
        if user_id:
            cursor.execute('''SELECT id, from_id, to_id, text, creation_data FROM messages
                           WHERE id=%s''', (user_id,))
        else:
            cursor.execute('SELECT id, from_id, to_id, text, creation_data FROM messages')
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_data = row
            loaded_message = Messages(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_data = creation_data
            messages.append(loaded_message)
        return messages






# def hash_password(password, salt=None):
# """
#     Hashes the password with salt as an optional parameter.
#
#     If salt is not provided, generates random salt.
#     If salt is less than 16 chars, fills the string to 16 chars.
#     If salt is longer than 16 chars, cuts salt to 16 chars.
#
#     :param str password: password to hash
#     :param str salt: salt to hash, default None
#
#     :rtype: str
#     :return: hashed password
#     """
#     if salt is None:
#         salt = generate_salt()
#     if len(salt) < 16:
#         salt += ("a" * (16 - len(salt)))
#     if len(salt) > 16:
#         salt = salt[:16]
#     t_sha = hashlib.sha256()
#     t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))
#
#     return salt + t_sha.hexdigest()
#
# def generate_salt():
#     """
#     Generates a 16-character random salt.
#
#     :rtype: str
#     :return: str with generated salt
#     """
#     salt = ""
#     for i in range(0, 16):
#
#         # get a random element from the iterable
#         salt += random.choice(ALPHABET)
#     return salt
