
class Aplication:
    def inicio():
        print("\n---------------------------Iniciando la aplicación---------------------------")
        print("\nQue desea hacer?")
        print("\n\t1. Registrarse")
        print("\n\t2. Iniciar sesión")
        print("\n\t3. Salir")
    
        comando = input("\nIngrese el número de la acción que desea realizar: ")

        if comando == "1":
            Aplication.registro()
        elif comando == "2":
            Aplication.iniciar_sesion()
        elif comando == "3":
            print("\n--------------------------Saliendo de la aplicación--------------------------")
        else:
            print("\nComando no válido")
            Aplication.inicio()
    
    def registro():
        print("\n------------------------------Registro------------------------------")
        usuario = input("\nIngrese el nombre de usuario: ")
        contraseña = input("\nIngrese la contraseña: ")
        confirmar_contraseña = input("\nConfirme la contraseña: ")

        while contraseña != confirmar_contraseña:
            print("\nLas contraseñas no coinciden")
            contraseña = input("\nIngrese la contraseña: ")
            confirmar_contraseña = input("\nConfirme la contraseña: ")
            
        print("\nUsuario registrado con éxito")

    def iniciar_sesion():
        print("\n---------------------------Inicio de sesión---------------------------")

