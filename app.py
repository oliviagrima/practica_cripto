from registro_bbdd import Base_datos
import getpass

class Aplication:
    def __init__(self):
        self.seguir_en_inicio = True

    def inicio(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tIniciando la aplicación\n------------------------------------------------------------------------------------------------------------\n")

        while self.seguir_en_inicio:
            try:
                print("\nQue desea hacer?")
                print("\n\t1. Registrarse")
                print("\n\t2. Iniciar sesión")
                print("\n\t3. Salir")
                comando = input("\nIngrese el número de la acción que desea realizar: ")
                if comando == "1":
                    self.registro() 
                elif comando == "2":
                    self.iniciar_sesion()
                elif comando == "3":
                    print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSaliendo de la aplicación \n------------------------------------------------------------------------------------------------------------")
                    self.seguir_en_inicio = False
                else:
                    print("\n------------------------------------------------------Comando no válido------------------------------------------------------")
                    comando = input("\nPor favor, ingrese un número del 1 al 3: ")
                    if comando == "1":
                        self.registro()
                    elif comando == "2":
                        self.iniciar_sesion()
                    elif comando == "3":
                        print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSaliendo de la aplicación \n------------------------------------------------------------------------------------------------------------")
                        self.seguir_en_inicio = False

            except KeyboardInterrupt:
                print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tSaliendo de la aplicación \n------------------------------------------------------------------------------------------------------------")
                self.seguir_en_inicio = False

    def registro(self):
        print("\n-------------------------------------Registro-------------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        
        while Base_datos.confirmar_usuario(usuario):
            print("\n---------------------Este usuario ya existe, por favor, ingrese otro nombre de usuario---------------------")
            usuario = input("\nIngrese el nombre de usuario: ")

        contraseña_adecuada= False
        while not contraseña_adecuada:
            contraseña = getpass.getpass("\nIngrese la contraseña: ")

            if usuario == "" or contraseña == "":
                print("\n-------------------------------------Por favor, complete todos los campos-------------------------------------")

            if len(contraseña)<8:
                print("\n------La longitud de la contraseña debe ser de 8 caracteres como mínimo, intentelo de nuevo------")
            
            else:
                contraseña_adecuada = True
        
        confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")

        while contraseña != confirmar_contraseña:
            print("\n----------------Las contraseñas no coinciden, por favor, vuelva a intentarlo----------------")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")
            confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")
        
        salt = Base_datos.generador_salt()

        token = Base_datos.generador_token(usuario, contraseña.encode(), salt)

        Base_datos.guardar_json_salt_token(usuario, salt, token)

        print("\n-------------------------------------Usuario registrado con éxito-------------------------------------")

    def iniciar_sesion(self):
        print("\n-------------------------------------Inicio de sesión-------------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        contraseña = getpass.getpass("\nIngrese la contraseña: ")

        if Base_datos.confirmar_usuario(usuario):

            salt_guardado = Base_datos.sacar_json_salt(usuario)

            token_nuevo = Base_datos.generador_token(usuario, contraseña.encode(), bytes.fromhex(salt_guardado)).hex()

            token_guardado = Base_datos.sacar_json_token(usuario)

            if token_nuevo == token_guardado:
                self.seguir_en_inicio = False
                self.juego()
            else:
                print("\n-------------------------------------Usuario o contraseña incorrectos-------------------------------------")

        else:
            print("\n-------------------------El usuario no existe en nuestra base de datos, debe registrarse-------------------------")


    def juego(self):
        print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\tBIENVENIDO AL MADRID STARS\n------------------------------------------------------------------------------------------------------------")
        seguir_en_juego = True
        while seguir_en_juego:
            try:
                print("\nQue desea hacer?")
                print("\n\t1. Ver mercado de fichajes")
                print("\n\t2. Ver tu equipo")
                print("\n\t3. Salir")
                comando = input("\nIngrese el número de la acción que desea realizar: ")
                if comando == "1":
                    self.mercado() 
                elif comando == "2":
                    self.equipo()
                elif comando == "3":
                    print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSaliendo del juego \n------------------------------------------------------------------------------------------------------------")
                    seguir_en_juego = False
                    self.seguir_en_inicio = True

            except KeyboardInterrupt:
                print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSaliendo del juego \n------------------------------------------------------------------------------------------------------------")
                seguir_en_juego = False
                self.seguir_en_inicio = True

    def mercado(self):
        print("\n-------------------------------------MERCADO DE FICHAJES-------------------------------------")
    
    def equipo(self):
        print("\n-------------------------------------TU EQUIPO-------------------------------------")
