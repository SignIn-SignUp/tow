
from os import path
import os

from .aes import encrypt, decrypt


class Tokendir:

    def __init__(self, base) -> None:
        self.dirpath = base

    def exists(self):
        return path.exists(path.join(self.dirpath, 'token'))

    def get(self, password: str):
        with open(path.join(self.dirpath, 'token'), 'r') as f:
            return decrypt(password, f.read())

    def put(self, password: str, token: str) -> None:
        if not path.exists(self.dirpath):
            os.makedirs(self.dirpath)
        with open(path.join(self.dirpath, 'token'), 'w') as f:
            enc = encrypt(pw=password, plain_text=token)
            f.write(enc)
