class User:
    def __init__(self, username, hashed_password):
        self._id = -1
        self.username = username
        self._hashed_password = hashed_password

    @property
    def get_id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password
   