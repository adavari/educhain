import os
import struct
from utils.number_utils import random_digit
from Crypto.Cipher import AES
import time
import json
import base64

KEY = os.getenv("ENCRYPTION_KEY")
IV = os.getenv("ENCRYPTION_IV")


def encrypt_file(key, iv, in_filename, out_filename=None, chunksize=64 * 1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.
        key:
            The encryption key - a bytes object that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.
        in_filename:
            Name of the input file
        out_filename:
            If None, '<in_filename>.enc' will be used.
        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename

    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_size = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', file_size))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    return out_filename


def decrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(original_size)
    return out_filename


def create_reset_password_token(user_id: str):
    code = random_digit()
    valid_time = int(time.time()) + (10 * 60)

    encryptor = AES.new(bytes.fromhex(KEY), AES.MODE_CBC, bytes.fromhex(IV))
    data = json.dumps({'user_id': user_id, 'code': code, 'time': valid_time}).encode()

    length = 16 - (len(data) % 16)
    data += bytes([length]) * length

    token = encryptor.encrypt(data)
    return {'token': base64.b64encode(token).decode(), 'code': code}


def validate_password_reset_token(user_id: str, code: str, token: str):
    t = int(time.time())
    encryptor = AES.new(bytes.fromhex(KEY), AES.MODE_CBC, bytes.fromhex(IV))
    data = encryptor.decrypt(base64.b64decode(token.encode()))
    data = data[:-data[-1]]
    json_data = data.decode()

    dic = json.loads(json_data)
    uid = dic['user_id']
    c = dic['code']
    valid_time = dic['time']
    if valid_time < t:
        return False

    if uid != user_id:
        return False

    if c != code:
        return False

    return True
