from registro_bbdd import Base_datos
from encriptacion import Encriptar
import getpass
import random
import json
import base64

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
                print("\n------------La longitud de la contraseña debe ser de 8 caracteres como mínimo, inténtelo de nuevo------------")
            
            else:
                contraseña_adecuada = True
        
        confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")

        while contraseña != confirmar_contraseña:
            print("\n-------------------------Las contraseñas no coinciden, por favor, vuelva a intentarlo-------------------------")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")
            confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")
        
        clave_encriptacion = Encriptar.generador_clave()
        Base_datos.guardar_json_clave(usuario, clave_encriptacion)
        salt = Encriptar.generador_salt(usuario)
        salt_base64 = base64.urlsafe_b64encode(salt)
        salt_cifrado = Encriptar.encriptar(salt_base64, usuario)
        token = Encriptar.generador_token(usuario, contraseña.encode(), salt)
        Base_datos.guardar_json_salt_token(usuario, salt_cifrado, token)
        
        Base_datos.crear_equipo(usuario)

        print("\n----------------------------------------Usuario registrado con éxito----------------------------------------")

    def iniciar_sesion(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tINICIO DE SESIÓN \n------------------------------------------------------------------------------------------------------------")
        inicio_correcto = False

        while not inicio_correcto:
            usuario = input("\nIngrese el nombre de usuario: ")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")

            if Base_datos.confirmar_usuario(usuario):
                salt_guardado = Base_datos.sacar_json_salt(usuario)
                salt_guardado_descifrado_base64 = Encriptar.desencriptar(bytes.fromhex(salt_guardado), usuario)
                salt_original = base64.urlsafe_b64decode(salt_guardado_descifrado_base64)
                
                token_nuevo = Encriptar.generador_token(usuario, contraseña.encode(), salt_original)
                token_nuevo_descifrado = Encriptar.desencriptar(token_nuevo, usuario).hex()
               
                token_guardado = Base_datos.sacar_json_token(usuario)
                token_guardado_descifrado = Encriptar.desencriptar(bytes.fromhex(token_guardado), usuario).hex()
                
                if token_nuevo_descifrado == token_guardado_descifrado:
                    self.seguir_en_inicio = False
                    inicio_correcto = True
                    self.juego(usuario)
                else:
                    print("\n-----------------------------Usuario o contraseña incorrectos, inténtelo de nuevo-----------------------------")

            else:
                print("\n-----------------El usuario no existe en nuestra base de dato o la contraseña es incorrecta-----------------")
                inicio_correcto = True #tengo que poner que se ha iniciado correctamente para poder volver a la pantalla de registro
                self._seguir_en_inicio = True


    def juego(self, usuario):
        print("------------------------------------------------------------------------------------------------------------")
        print("\t\t\t▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▄  ▗▄▖")
        print("\t\t\t▐▌ ▐▌  █  ▐▌   ▐▛▚▖▐▌▐▌  ▐▌▐▌   ▐▛▚▖▐▌  █  ▐▌  █▐▌ ▐▌")
        print("\t\t\t▐▛▀▚▖  █  ▐▛▀▀▘▐▌ ▝▜▌▐▌  ▐▌▐▛▀▀▘▐▌ ▝▜▌  █  ▐▌  █▐▌ ▐▌")
        print("\t\t\t▐▙▄▞▘▗▄█▄▖▐▙▄▄▖▐▌  ▐▌ ▝▚▞▘ ▐▙▄▄▖▐▌  ▐▌▗▄█▄▖▐▙▄▄▀▝▚▄▞▘")
        print("------------------------------------------------------------------------------------------------------------")
        seguir_en_juego = True
        while seguir_en_juego:
            try:
                print("\nQUÉ DESEA HACER?")
                print("\n\t1. Ver mercado de fichajes")
                print("\n\t2. Ver equipo")
                print("\n\t3. Ver saldo disponible")
                print("\n\t4. Salir")
                comando = input("\nIngrese el número de la acción que desea realizar: ")
                if comando == "1":
                    self.mercado(usuario) 
                elif comando == "2":
                    self.equipo(usuario)
                elif comando == "3":
                    print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALDO DISPONIBLE \n------------------------------------------------------------------------------------------------------------")
                    if Base_datos.mostrar_saldo(usuario) > 0:
                        print("Tiene", Base_datos.mostrar_saldo(usuario), "M€")
                        print("------------------------------------------------------------------------------------------------------------")
                    else:
                        print("\n------------------------------------------No le queda saldo------------------------------------------")
    
                elif comando == "4":
                    print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALIENDO DEL JUEGO \n------------------------------------------------------------------------------------------------------------")
                    seguir_en_juego = False
                    self.seguir_en_inicio = True
                else:
                    print("\n---------------------------------------------Comando no válido---------------------------------------------")
                    comando = input("\nPor favor, ingrese un número del 1 al 3: ")
                    if comando == "1":
                        self.mercado(usuario) 
                    elif comando == "2":
                        self.equipo(usuario)
                    elif comando == "3":
                        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALDO DISPONIBLE \n------------------------------------------------------------------------------------------------------------")
                        if Base_datos.mostrar_saldo(usuario) > 0:
                            print("Tiene", Base_datos.mostrar_saldo(usuario), "M€")
                            print("------------------------------------------------------------------------------------------------------------")
                        else:
                            print("\n------------------------------------------No le queda saldo------------------------------------------")
                    elif comando == "4":
                        print("------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALIENDO DEL JUEGO \n------------------------------------------------------------------------------------------------------------")
                        seguir_en_juego = False
                        self.seguir_en_inicio = True

            except KeyboardInterrupt:
                print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tSALIENDO DEL JUEGO \n------------------------------------------------------------------------------------------------------------")
                seguir_en_juego = False
                self.seguir_en_inicio = True

    def mercado(self, usuario):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tMERCADO DE FICHAJES \n------------------------------------------------------------------------------------------------------------")
        lista_jugadores = ["Vini Jr", "Mbappe", "Rodrygo", "Bellingham", "Modric", "Valverde", "F. Mendy", "Rudiger", "E. Militao", "Carvajal", "Courtois"]
        print("\nJUGADORES DISPONIBLES:")
        jugadores_aleatorios = random.sample(lista_jugadores, 3)
        indice = 1

        precios_jugadores = {}
        for jugador in jugadores_aleatorios:
            precios_jugadores[jugador] = random.randint(2, 5)
            print("\n\t",indice, "→", jugador, ":", precios_jugadores[jugador], "M€")
            indice += 1 

        acabar_pregunta = False
        while not acabar_pregunta:
            saldo_usuario = Base_datos.mostrar_saldo(usuario)
            print("\nSaldo disponible: ", saldo_usuario, "M€")
            compra = input("\nDESEA COMPRAR ALGÚN JUGADOR? (si/no): ").lower()
            if compra == "si":
                self.comprar_jugador(usuario, jugadores_aleatorios, precios_jugadores)
                acabar_pregunta = True

            elif compra == "no":
                print("\n---------------------------------------No ha comprado ningún jugador---------------------------------------")
                acabar_pregunta = True
            
            else:
                print("\n---------------------------------------------Comando no válido---------------------------------------------")
                compra = input("\nPor favor, ingrese 'si' o 'no': ")
                if compra == "si":
                    self.comprar_jugador(usuario, jugadores_aleatorios, precios_jugadores)
                    acabar_pregunta = True

                elif compra == "no":
                    print("\n----------------------------------------No ha comprado ningún jugador----------------------------------------")
                    acabar_pregunta = True
                

    def comprar_jugador(self, usuario, jugadores_aleatorios, precios_jugadores):
        print("\n-----------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tCOMPRAR JUGADOR \n-----------------------------------------------------------------------------------------------------------")
        
        jugador_comprado = input("\nIngrese el nombre del jugador que desea comprar: ")
        compra_de_jugadores = True

        while compra_de_jugadores:
            if jugador_comprado in jugadores_aleatorios:
                precio_jugador = precios_jugadores[jugador_comprado]
                Base_datos.fichar_jugador(usuario, jugador_comprado, precio_jugador)
                compra_de_jugadores = False
            else:
                print("\n------------------------------------Jugador no disponible en el mercado------------------------------------")
                jugador_comprado = input("\nIngrese el nombre del jugador que desea comprar: ")
    
    def equipo(self, usuario):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tTU EQUIPO \n------------------------------------------------------------------------------------------------------------")
        print("\nJUGADORES DE TU EQUIPO: \n")
        Base_datos.visualizar_equipo(usuario)
        print("\n------------------------------------------------------------------------------------------------------------")
        