import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class Base_datos:
    def confirmar_usuario(usuario):
        try:
            f = open("base_de_datos/clientes.json", "r")
            with open("base_de_datos/clientes.json", "r") as f:
                data = json.load(f)
                if usuario in data:
                    return True
                    #print("\nEste usuario ya existe, por favor, ingrese otro nombre de usuario")
                    #usuario = input("\nIngrese el nombre de usuario: ")
                    #Base_datos.confirmar_usuario(usuario)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        f.close()
    
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

    def sacar_json_salt(usuario):
        with open("base_de_datos/clientes.json", "r") as f:
            data = json.load(f)
            salt = data[usuario]["salt"]
        return salt
    
    def sacar_json_token(usuario):
        with open("base_de_datos/clientes.json", "r") as f:
            data = json.load(f)
            token = data[usuario]["token"]
        return token
        