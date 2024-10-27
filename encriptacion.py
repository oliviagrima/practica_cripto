import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


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
    
    def generador_clave_chacha20_poly():
        # Genera una clave de 256 bits (32 bytes) para ChaCha20-Poly1305
        clave = os.urandom(32)
        return clave

    def encriptar_mensaje(clave, mensaje, num_unico):
        # Cifra el mensaje usando ChaCha20-Poly1305
        chacha = ChaCha20Poly1305(clave)
        mensaje_cifrado = chacha.encrypt(num_unico, mensaje.encode(), None)
        return mensaje_cifrado

    def desencriptar_mensaje(clave, mensaje_cifrado, num_unico):
        # Descifra el mensaje usando ChaCha20-Poly1305
        chacha = ChaCha20Poly1305(clave)
        mensaje_descifrado = chacha.decrypt(num_unico, mensaje_cifrado, None)
        return mensaje_descifrado.decode()