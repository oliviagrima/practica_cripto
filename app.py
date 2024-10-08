
class Aplication:
    def inicio(self):
        print("\n---------------------------Iniciando la aplicación---------------------------")
        print("\nQue desea hacer?")
        print("\n\t1. Registrarse")
        print("\n\t2. Iniciar sesión")
        print("\n\t3. Salir")

        seguir_en_app = True
        while seguir_en_app:
            try:
                comando = input("\nIngrese el número de la acción que desea realizar: ")

                if comando == "1":
                    self.registro() 
                elif comando == "2":
                    self.iniciar_sesion()
                elif comando == "3":
                    print("\n---------------------------Saliendo de la aplicación---------------------------")
                    seguir_en_app = False
                else:
                    comando = input("\nComando no válido, por favor, ingrese un número del 1 al 3: ")
                    if comando == "1":
                        self.registro()
                    elif comando == "2":
                        self.iniciar_sesion()
                    elif comando == "3":
                        print("\n---------------------------Saliendo de la aplicación---------------------------")
                        seguir_en_app = False

            except KeyboardInterrupt:
                print("\n---------------------------Saliendo de la aplicación---------------------------")
                seguir_en_app = False

    def registro(self):
        print("\n------------------------------Registro------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        contraseña = input("\nIngrese la contraseña: ")
        confirmar_contraseña = input("\nConfirme la contraseña: ")

        if usuario == "" or contraseña == "" or confirmar_contraseña == "":
            print("\nPor favor, complete todos los campos")

        #if usuario == un usuario ya registrado --> error

        while contraseña != confirmar_contraseña:
            print("\nLas contraseñas no coinciden, por favor, vuelva a intentarlo")
            contraseña = input("\nIngrese la contraseña: ")
            confirmar_contraseña = input("\nConfirme la contraseña: ")
            
        print("\nUsuario registrado con éxito")

    def iniciar_sesion(self):
        print("\n---------------------------Inicio de sesión---------------------------")

