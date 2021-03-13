import random
from psycopg2 import connect

class User:
    con = connect(user='postgres', host='localhost', password='coderslab',
                  database='workshops_module2')
    con.autocommit = True
    cursor = con.cursor()

    def __init__(self, username='', hashed_password=''):
        self._id = -1
        self.username = username
        self._hashed_password = hashed_password

    @property
    def get_id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password
    #we need this function because in the end we want to store
    #only the hashed value of the password
    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            cursor.execute('''INSERT INTO users (username, hashed_password) VALUES (%s, %s)
                           RETURNING id''', (self.username, self.hashed_password))
            self._id = cursor.fetchone()[0]
            return True
        return False



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
