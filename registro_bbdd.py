import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class Base_datos:
    
    def generador_salt():
        salt = os.urandom(16)
        return salt

    def generador_token(usuario, contraseña, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        token = base64.urlsafe_b64encode(kdf.derive(contraseña))
        return token
    
    def guardar_json_salt_token(usuario, salt, token):
        f = open("base_de_datos/clientes.json", "r")
        try:
            with open("base_de_datos/clientes.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        data[usuario] = {
            "salt": salt.hex(),
            "token": token.hex()
        }

        with open("base_de_datos/clientes.json", "w") as file:
            json.dump(data, file, indent=4)
        
        f.close()

        