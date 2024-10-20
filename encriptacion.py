import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from registro_bbdd import Base_datos

class Encriptar:

    def generador_salt():
        salt = os.urandom(16)
        #salt_cifrado = Encriptar.encriptar_salt(salt)
        return salt

    def generador_token(usuario, contraseña, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        token = base64.urlsafe_b64encode(kdf.derive(contraseña))
        #f = Fernet(token)
        #token_cifrado = Encriptar.encriptar_token(token)
        return token
"""   
    def generador_clave(contraseña, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(contraseña))
        return Fernet(key)
   
    def encriptar_token(token, contraseña, salt):
        f = Encriptar.generador_clave(contraseña, salt)
        token_cifrado = f.encrypt(token)
        return token_cifrado

    def encriptar_salt(salt, contraseña):
        f = Encriptar.generador_clave(contraseña, salt)
        salt_cifrado = f.encrypt(salt)
        return salt_cifrado
   
    def desencriptar_salt(salt_cifrado, key):
        f = Fernet(key)
        salt = f.decrypt(salt_cifrado)
        return salt
   
    def desencriptar_token(token_cifrado, key):
        f = Fernet(key)
        token = f.decrypt(token_cifrado)
        return token
"""






        
      