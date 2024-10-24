import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from registro_bbdd import Base_datos

class Encriptar:

    def generador_clave():
        key = Fernet.generate_key()
        return key
    
    def generador_salt(usuario):
        salt = os.urandom(32)
        return salt

    def generador_token(usuario, contraseña, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        token = base64.urlsafe_b64encode(kdf.derive(contraseña))
        token_cifrado = Encriptar.encriptar(token, usuario)
        return token_cifrado
    
    def encriptar(input, usuario):
        key = Base_datos.sacar_json_clave(usuario)
        f = Fernet(key)
        input_cifrado = f.encrypt(input)
        return input_cifrado
    
    def desencriptar(input_cifrado, usuario):
        key = Base_datos.sacar_json_clave(usuario)
        f = Fernet(key)
        input = f.decrypt(input_cifrado)
        return input
