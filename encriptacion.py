import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.backends import default_backend


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
        return token
    
    def encriptar(fichero, f):
        fichero_cifrado = f.encrypt(fichero)
        return fichero_cifrado
    
    def desencriptar(fichero_cifrado, f):
        fichero = f.decrypt(fichero_cifrado)
        return fichero

    def generador_clave_aes():
        clave = os.urandom(32)
        return clave
    
    def generador_cmac(mensaje, clave):
        cmac = CMAC(algorithms.AES(clave), backend=default_backend())
        cmac.update(mensaje)
        return cmac.finalize()
    
    def comprobar_cmac(mensaje, clave, cmac_original):
        cmac2 = CMAC(algorithms.AES(clave), backend=default_backend())
        cmac2.update(mensaje)
        try:
            cmac2.verify(cmac_original)
            return True
        except:
            return False