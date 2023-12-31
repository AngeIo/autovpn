#!/usr/bin/python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os.path
import sys
import getpass

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

# Generate a key and store it in a file
def mykeygen() -> bytes:
    # Does the key already exists?
    if os.path.isfile(".key"):
        # If yes, read it
        with open(".key", "rb") as file:
            key = file.read()
    else:
        # If no, generate it and write it in a file
        key = Fernet.generate_key()  # store in a secure location
        with open(".key", "wb") as file:
            file.write(key)
    if type(key) != bytes:
        key = key.encode("utf-8")
    return key

def keyencrypt(my_pw, mykey):
    # Encrypt the password and show the result
    encrypted_text = encrypt(my_pw.encode(), mykey).decode("utf-8")
    print(f"Encrypted password to copy paste in the 'variables.py' file:\n\n{encrypted_text}")

def main():
    # Get the key or generate it
    mykey = mykeygen()
    # Read the password to encrypt
    if len(sys.argv) == 2:
        my_pw = sys.argv[1]
        keyencrypt(my_pw, mykey)
    # If there are no arguments, then ask the string to be converted on the command line
    elif len(sys.argv) == 1:
        my_pw = getpass.getpass('Password to encrypt: ')
        keyencrypt(my_pw, mykey)
    else:
        print("Wrong number of arguments")
        print("Usage: python3 passwordman.py [password_to_encrypt]")

# ---

if __name__ == '__main__':
    main()
