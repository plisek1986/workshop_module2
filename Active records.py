from models import
from clcrypto import hash_password

class User:
    def __init__(self, username="", password="", salt=""):
        #Wartość id nadpiszemy podczas synchronizacji.
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    #setter nie ma możliwości przekazania parametru salt, dlatego tworzymy do tego celu poniższą metodę
    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    # setter, który generuje sól automatycznie
    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    #synchronizowanie obiektu z bazą danych
    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            # Jeżeli udało się nam zapisać obiekt do bazy, to przypisujemy mu klucz główny jako id.
            # Jeśli się nie uda, to Python zgłosi wyjątek.
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        return False

    #pobieranie jednego obiektu z bazy danych
    @staticmethod
    #argumentem jest też obiekt kursora
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            #rozpakowujemy dane do odpowiednich zmiennych
            id_, username, hashed_password = data
            #tworzymy nowy obiekt użytkownika - tutaj self jest zastąpione username, bo odnosimy się do
            #obiektu username danej klasy
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    #--------------------------------------------------------------------------
    #pobieranie wszystkich obiektów z bazy danych
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        #tworzymy pustą listę, którą póżniej wypełnimy  obiektami z bazy dancyh
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    #----------------------------------------------------------
    # modyfikacja już istniejącego obiektu
    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True
    #-------------------------------------------------------------
    # usunięcie obiektu z bazy danych
    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

