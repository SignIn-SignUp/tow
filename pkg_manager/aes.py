from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from base64 import b64encode, b64decode

BLOCK_SIZE = AES.block_size
SALT_LEN = 16
HASH_LEN = 32
CPU_MEM_COST = 2**20
SRCYPT_BLOCKSIZE = 8
SCRYPT_PAR = 1


def encrypt(pw, plain_text):
    salt, key = __hash_key(pw)
    plain_text = __pad(plain_text)
    iv = Random.get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(key + plain_text.encode())
    return b64encode(salt + iv + encrypted_text).decode("utf-8")


def decrypt(key, encrypted_text):
    encrypted_text = b64decode(encrypted_text)
    iv = encrypted_text[SALT_LEN:SALT_LEN + BLOCK_SIZE]
    salt = encrypted_text[:SALT_LEN]
    _, key = __hash_key(key=key, salt=salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(
        encrypted_text[SALT_LEN + BLOCK_SIZE:])
    if not decrypted_text[:HASH_LEN] == key:
        return None
    plain_text = decrypted_text[HASH_LEN:].decode("utf-8")
    return __unpad(plain_text)


def __pad(plain_text):
    number_of_bytes_to_pad = BLOCK_SIZE - len(plain_text) % BLOCK_SIZE
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    padded_plain_text = plain_text + padding_str
    return padded_plain_text


def __unpad(plain_text):
    last_character = plain_text[len(plain_text) - 1:]
    return plain_text[:-ord(last_character)]


def __hash_key(key: str, salt: str = Random.get_random_bytes(SALT_LEN)) -> tuple[bytes, bytes]:
    key = scrypt(
        password=key.encode(),
        salt=salt,
        key_len=HASH_LEN,
        N=CPU_MEM_COST,
        r=SRCYPT_BLOCKSIZE,
        p=SCRYPT_PAR
    )
    return (salt, key)
