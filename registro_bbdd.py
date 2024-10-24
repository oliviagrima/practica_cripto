import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class Base_datos:
    def confirmar_usuario(usuario):
        try:
            with open("base_de_datos/clientes.json", "r") as f:
                data = json.load(f)
                if usuario in data:
                    return True
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        f.close()
    
    def guardar_json_clave(usuario, clave):
        clave_base64 = base64.urlsafe_b64encode(clave).hex()
        try:
            with open("base_de_datos/claves_clientes.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        data[usuario] = {
            "clave": clave_base64
        }

        with open("base_de_datos/claves_clientes.json", "w") as file:
            json.dump(data, file, indent=4)
        
        f.close()

    def guardar_json_salt_token(usuario, salt, token):
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

    def sacar_json_clave(usuario):
        with open("base_de_datos/claves_clientes.json", "r") as f:
            data = json.load(f)
            clave = base64.urlsafe_b64decode(bytes.fromhex(data[usuario]["clave"]))
        return clave

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
    
    def crear_equipo(usuario):
        try:
            with open("base_de_datos/equipos_usuarios.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}
        
        if usuario not in data:
            data[usuario] = {"saldo": 40,
                             "equipo": []}

        with open("base_de_datos/equipos_usuarios.json", "w") as f:
            json.dump(data, f, indent=4)
        
        f.close()
    
    def mostrar_saldo(usuario):
        with open("base_de_datos/equipos_usuarios.json", "r") as f:
            data = json.load(f)
            saldo = data[usuario]["saldo"]
        return saldo

    def fichar_jugador(usuario, jugador_comprado, precio_jugador):
        try:
            with open("base_de_datos/equipos_usuarios.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        saldo_usuario = data[usuario]["saldo"]

        if saldo_usuario >= precio_jugador:
            if jugador_comprado not in data[usuario]["equipo"]:
                data[usuario]["saldo"] -= precio_jugador
                data[usuario]["equipo"].append(jugador_comprado)
                print("\n------------------------------------Ha comprado a ",jugador_comprado," por",precio_jugador,"M€-------------------------------------")
            else:
                print("\n---------------------Ya tiene este jugador en tu equipo, no puede volver a comprarlo---------------------")
        else:
            print("\n------------------------No tiene suficiente saldo para fichar a ", jugador_comprado, "------------------------")
        with open("base_de_datos/equipos_usuarios.json", "w") as f:
            json.dump(data, f, indent=4)
        
        f.close()

    def visualizar_equipo(usuario):
        f = open("base_de_datos/equipos_usuarios.json", "r")
        with open("base_de_datos/equipos_usuarios.json", "r") as f:
            data = json.load(f)

            equipo = data[usuario]["equipo"]
            if not equipo:
                print("No tienes ningún fichaje todavía.")
            else:
                for jugador in equipo:
                    print("\t- ", jugador)
        f.close()