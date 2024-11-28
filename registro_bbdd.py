import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509 import load_pem_x509_certificate
import json
from encriptacion import Encriptar
from cryptography.fernet import Fernet
import os

class Base_datos:
 
    def comprobar_fichero_encriptado():
        try:
            with open("base_de_datos/clientes.json", 'r') as file:
                json.load(file)
            return False
        except json.JSONDecodeError:
            return True  
        
    def comprobar_fichero_vacio():
        with open("base_de_datos/clientes.json", 'r') as file:
            if file.read() == "":
                return True
            else:
                return False
 
    def encriptar_fichero():
        key = Base_datos.sacar_json_clave()
        f = Fernet(key)
        with open("base_de_datos/clientes.json", "rb") as file:
            fichero = file.read()
        fichero_encriptado = Encriptar.encriptar(fichero, f)

        with open("base_de_datos/clientes.json", "wb") as file:
            file.write(fichero_encriptado)
        file.close()

    def desencriptar_fichero():
        key = Base_datos.sacar_json_clave()
        f = Fernet(key)
        with open("base_de_datos/clientes.json", "rb") as file:
            fichero_encriptado = file.read()
        fichero = Encriptar.desencriptar(fichero_encriptado, f)

        with open("base_de_datos/clientes.json", "wb") as file:
            file.write(fichero)
        file.close()

    def confirmar_usuario(usuario):
        try:
            with open("base_de_datos/clientes.json", "r") as f:
                data = json.load(f)
                if usuario in data:
                    return True
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            pass
    
    def guardar_json_clave(clave):
        clave_base64 = base64.urlsafe_b64encode(clave).hex()
        try:
            with open("base_de_datos/clave_encriptacion.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}

        if not data:
            data = {
                "clave": clave_base64
            }

        with open("base_de_datos/clave_encriptacion.json", "w") as file:
            json.dump(data, file, indent=4)

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
        

    def sacar_json_clave():
        with open("base_de_datos/clave_encriptacion.json", "r") as f:
            data = json.load(f)
            clave = base64.urlsafe_b64decode(bytes.fromhex(data["clave"]))
        return clave

    def sacar_json_salt(usuario):
        with open("base_de_datos/clientes.json", "r") as f:
            data = json.load(f)
            salt_hex = data[usuario]["salt"]
            salt = bytes.fromhex(salt_hex)
        return salt
    
    def sacar_json_token(usuario):
        with open("base_de_datos/clientes.json", "r") as f:
            data = json.load(f)
            token = data[usuario]["token"]
        return token
    
    def crear_carpeta_equipo_usuario(usuario):
        os.makedirs("base_de_datos/equipos_usuarios", exist_ok=True)
        ruta_archivo = f"base_de_datos/equipos_usuarios/equipo_{usuario}.json"

        try:
            with open(ruta_archivo, "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}
            data[usuario] = {"saldo": 40,
                             "equipo": []}

        with open(ruta_archivo, "w") as f:
            json.dump(data, f, indent=4)
    
    
    def mostrar_saldo(usuario):
        ruta_archivo = f"base_de_datos/equipos_usuarios/equipo_{usuario}.json"
        with open(ruta_archivo, "r") as f:
            data = json.load(f)
            saldo = data[usuario]["saldo"]
        return saldo

    def fichar_jugador(usuario, jugador_comprado, precio_jugador):
        ruta_archivo = f"base_de_datos/equipos_usuarios/equipo_{usuario}.json"
        try:
            with open(ruta_archivo, "r") as f:
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
        with open(ruta_archivo, "w") as f:
            json.dump(data, f, indent=4)
        

    def visualizar_equipo(usuario):
        ruta_archivo = f"base_de_datos/equipos_usuarios/equipo_{usuario}.json"
        f = open(ruta_archivo, "r")
        with open(ruta_archivo, "r") as f:
            data = json.load(f)

            equipo = data[usuario]["equipo"]
            if not equipo:
                print("No tienes ningún fichaje todavía.")
            else:
                for jugador in equipo:
                    print("\t- ", jugador)

    def guardar_json_claves_servidor(clave_privada, clave_publica, certificado):
        private_pem = clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = clave_publica.public_bytes(	
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        certificado_pem = certificado.public_bytes(
            encoding=serialization.Encoding.PEM 
        )

        try:
            with open("base_de_datos/claves_servidor.json", "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}
            data["clave_publica"] = public_pem.decode()
            data["clave_privada"] = private_pem.decode()
            data["certificado"] = certificado_pem.decode()

        with open("base_de_datos/claves_servidor.json", "w") as f:
            json.dump(data, f, indent=4)

    def guardar_json_claves_usuario(usuario, clave_privada, clave_publica, certificado):
        private_pem = clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = clave_publica.public_bytes(	
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        certificado_pem = certificado.public_bytes(
            encoding=serialization.Encoding.PEM
        )

        os.makedirs("base_de_datos/claves_usuarios", exist_ok=True)
        ruta_archivo = f"base_de_datos/claves_usuarios/claves_{usuario}.json"

        try:
            with open(ruta_archivo, "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}
            data[usuario] = {"clave_publica": public_pem.decode(),
                             "clave_privada": private_pem.decode(),
                             "certificado": certificado_pem.decode()}

        with open(ruta_archivo, "w") as f:
            json.dump(data, f, indent=4)

    def guardar_json_claves_ACs(nombre_ac, clave_privada, clave_publica, certificado):
        private_pem = clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = clave_publica.public_bytes(	
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        certificado_pem = certificado.public_bytes(
            encoding=serialization.Encoding.PEM
        )

        os.makedirs("base_de_datos/claves_ACs", exist_ok=True)
        ruta_archivo = f"base_de_datos/claves_ACs/claves_{nombre_ac}.json"

        try:
            with open(ruta_archivo, "r") as f:
                data = json.load(f)
        except(json.decoder.JSONDecodeError, FileNotFoundError):
            data = {}
            data[nombre_ac] = {"clave_publica": public_pem.decode(),
                             "clave_privada": private_pem.decode(),
                             "certificado": certificado_pem.decode()}

        with open(ruta_archivo, "w") as f:
            json.dump(data, f, indent=4)

    def sacar_claves_intermedio_usuarios():
        with open("base_de_datos/claves_ACs/claves_FlorentinoPerez.json", "r") as f:
            data = json.load(f)
            clave_privada_intermedio_usuarios = serialization.load_pem_private_key(data["FlorentinoPerez"]["clave_privada"].encode(), password=None)
            certificado_intermedio_usuarios = load_pem_x509_certificate(data["FlorentinoPerez"]["certificado"].encode())
        return clave_privada_intermedio_usuarios, certificado_intermedio_usuarios
    
    def extraer_certificado_cliente(usuario):
        ruta_archivo = f"base_de_datos/claves_usuarios/claves_{usuario}.json"
        with open(ruta_archivo, "r") as f:
            data = json.load(f)
            certificado_cliente = load_pem_x509_certificate(data[usuario]["certificado"].encode())
        return certificado_cliente
    
    def extraer_certificado_servidor():
        with open("base_de_datos/claves_servidor.json", "r") as f:
            data = json.load(f)
            certificado_servidor = load_pem_x509_certificate(data["certificado"].encode())
        return certificado_servidor
    
    def extraer_certificado_intermedio_servidor():
        with open("base_de_datos/claves_ACs/claves_JavierTebas.json", "r") as f:
            data = json.load(f)
            certificado_intermedio_servidor = load_pem_x509_certificate(data["JavierTebas"]["certificado"].encode())
        return certificado_intermedio_servidor

    def extraer_certificado_intermedio_raiz():
        with open("base_de_datos/claves_ACs/claves_LaLiga.json", "r") as f:
            data = json.load(f)
            certificado_raiz = load_pem_x509_certificate(data["LaLiga"]["certificado"].encode())
        return certificado_raiz