import hashlib
import random
import string


# This function hashes a password using cryptography and additional salt values
def hash_password(password, salt=None):
    """
        Hashes the password with salt as an optional parameter.

        If salt is not provided, generates random salt.
        If salt is less than 16 chars, fills the string to 16 chars.
        If salt is longer than 16 chars, cuts salt to 16 chars.

        :param str password: password to hash
        :param str salt: salt to hash, default None

        :rtype: str
        :return: hashed password
        """
    if salt is None:
        salt = generate_salt()
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))
    if len(salt) > 16:
        salt = salt[:16]
    t_sha = hashlib.sha256()
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    return salt + t_sha.hexdigest()

    #we generate a correct sals in case the salt is not provided for hashing the password
def generate_salt():
    ALPHABET = list(string.ascii_lowercase)
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        # get a random element from the iterable
        salt += random.choice(ALPHABET)
    return salt
