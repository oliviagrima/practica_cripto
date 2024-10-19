from registro_bbdd import Base_datos
from encriptacion import Encriptar
import getpass

class Aplication:
    def __init__(self):
        self.seguir_en_inicio = True

    def inicio(self):
        print("------------------------------------------------------------------------------------------------------------")
        print("\t\t\t▗▖  ▗▖ ▗▄▖ ▗▄▄▄ ▗▄▄▖ ▗▄▄▄▖▗▄▄▄      ▗▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖  ▗▄▄")
        print("\t\t\t▐▛▚▞▜▌▐▌ ▐▌▐▌  █▐▌ ▐▌  █  ▐▌  █    ▐▌     █ ▐▌ ▐▌▐▌ ▐▌▐▌   ")
        print("\t\t\t▐▌  ▐▌▐▛▀▜▌▐▌  █▐▛▀▚▖  █  ▐▌  █     ▝▀▚▖  █ ▐▛▀▜▌▐▛▀▚▖ ▝▀▚▖")
        print("\t\t\t▐▌  ▐▌▐▌ ▐▌▐▙▄▄▀▐▌ ▐▌▗▄█▄▖▐▙▄▄▀    ▗▄▄▞▘  █ ▐▌ ▐▌▐▌ ▐▌▗▄▄▞▘")
        print("------------------------------------------------------------------------------------------------------------")
        while self.seguir_en_inicio:
            try:
                print("\nQUÉ DESEA HACER?")
                print("\n\t1. Registrarse")
                print("\n\t2. Iniciar sesión")
                print("\n\t3. Salir")
                comando = input("\nIngrese el número de la acción que desea realizar: ")
                if comando == "1":
                    self.registro() 
                elif comando == "2":
                    self.iniciar_sesion()
                elif comando == "3":
                    print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSALIENDO DE LA APLICACIÓN \n------------------------------------------------------------------------------------------------------------")
                    self.seguir_en_inicio = False
                else:
                    print("\n---------------------------------------------Comando no válido---------------------------------------------")
                    comando = input("\nPor favor, ingrese un número del 1 al 3: ")
                    if comando == "1":
                        self.registro()
                    elif comando == "2":
                        self.iniciar_sesion()
                    elif comando == "3":
                        print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSALIENDO DE LA APLICACIÓN \n------------------------------------------------------------------------------------------------------------")
                        self.seguir_en_inicio = False

            except KeyboardInterrupt:
                print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSALIENDO DE LA APLICACIÓN \n------------------------------------------------------------------------------------------------------------")
                self.seguir_en_inicio = False

    def registro(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tREGISTRO \n------------------------------------------------------------------------------------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        
        while Base_datos.confirmar_usuario(usuario):
            print("\n----------------------Este usuario ya existe, por favor, ingrese otro nombre de usuario----------------------")
            usuario = input("\nIngrese el nombre de usuario: ")

        contraseña_adecuada= False
        while not contraseña_adecuada:
            contraseña = getpass.getpass("\nIngrese la contraseña: ")

            if usuario == "" or contraseña == "":
                print("\n------------------------------------Por favor, complete todos los campos------------------------------------")

            if len(contraseña)<8:
                print("\n------------La longitud de la contraseña debe ser de 8 caracteres como mínimo, intentelo de nuevo------------")
            
            else:
                contraseña_adecuada = True
        
        confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")

        while contraseña != confirmar_contraseña:
            print("\n-------------------------Las contraseñas no coinciden, por favor, vuelva a intentarlo-------------------------")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")
            confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")
        
        salt = Encriptar.generador_salt()

        token = Encriptar.generador_token(usuario, contraseña.encode(), salt)

        Base_datos.guardar_json_salt_token(usuario, salt, token)

        print("\n----------------------------------------Usuario registrado con éxito----------------------------------------")

    def iniciar_sesion(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tINICIO DE SESIÓN \n------------------------------------------------------------------------------------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        contraseña = getpass.getpass("\nIngrese la contraseña: ")

        if Base_datos.confirmar_usuario(usuario):

            salt_guardado = Base_datos.sacar_json_salt(usuario)

            salt_guardado_descifrado = Encriptar.desencriptar_salt(bytes.fromhex(salt_guardado))

            token_nuevo = Encriptar.generador_token(usuario, contraseña.encode(), bytes.fromhex(salt_guardado_descifrado)).hex()

            token_nuevo_descifrado = Encriptar.desencriptar_token(bytes.fromhex(token_nuevo)).hex()

            token_guardado = Base_datos.sacar_json_token(usuario)

            token_guardado_descifrado = Encriptar.desencriptar_token(bytes.fromhex(token_guardado)).hex()

            if token_nuevo_descifrado == token_guardado_descifrado:
                self.seguir_en_inicio = False
                self.juego()
            else:
                print("\n-------------------------------------Usuario o contraseña incorrectos-------------------------------------")

        else:
            print("\n-----------------------El usuario no existe en nuestra base de datos, debe registrarse-----------------------")


    def juego(self):
        print("-------------------------------------------------------------------------------------------------------------")
        print("\t\t\t▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▄  ▗▄▖")
        print("\t\t\t▐▌ ▐▌  █  ▐▌   ▐▛▚▖▐▌▐▌  ▐▌▐▌   ▐▛▚▖▐▌  █  ▐▌  █▐▌ ▐▌")
        print("\t\t\t▐▛▀▚▖  █  ▐▛▀▀▘▐▌ ▝▜▌▐▌  ▐▌▐▛▀▀▘▐▌ ▝▜▌  █  ▐▌  █▐▌ ▐▌")
        print("\t\t\t▐▙▄▞▘▗▄█▄▖▐▙▄▄▖▐▌  ▐▌ ▝▚▞▘ ▐▙▄▄▖▐▌  ▐▌▗▄█▄▖▐▙▄▄▀▝▚▄▞▘")
        print("-------------------------------------------------------------------------------------------------------------")
        seguir_en_juego = True
        while seguir_en_juego:
            try:
                print("\nQUÉ DESEA HACER?")
                print("\n\t1. Ver mercado de fichajes")
                print("\n\t2. Ver tu equipo")
                print("\n\t3. Salir")
                comando = input("\nIngrese el número de la acción que desea realizar: ")
                if comando == "1":
                    self.mercado() 
                elif comando == "2":
                    self.equipo()
                elif comando == "3":
                    print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALIENDO DEL JUEGO \n------------------------------------------------------------------------------------------------------------")
                    seguir_en_juego = False
                    self.seguir_en_inicio = True

            except KeyboardInterrupt:
                print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALIENDO DEL JUEGO \n------------------------------------------------------------------------------------------------------------")
                seguir_en_juego = False
                self.seguir_en_inicio = True

    def mercado(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tMERCADO DE FICHAJES \n-----------------------------------------------------------------------------------------------------------")
    
    def equipo(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tTU EQUIPO \n-----------------------------------------------------------------------------------------------------------")
