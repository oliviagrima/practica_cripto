import os

class Base_datos():
    
    def generador_salt(self, username):
        salt = os.urandom(16)
        return salt

    def generador_token():
        ...