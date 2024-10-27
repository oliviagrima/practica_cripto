from registro_bbdd import Base_datos
from encriptacion import Encriptar
import getpass
import random
import os

class Aplicacion:

    def __init__(self):
        self.seguir_en_inicio = True

    def inicio(self):
        print("------------------------------------------------------------------------------------------------------------")
        print("\t\t\t▗▖  ▗▖ ▗▄▖ ▗▄▄▄ ▗▄▄▖ ▗▄▄▄▖▗▄▄▄      ▗▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖  ▗▄▄")
        print("\t\t\t▐▛▚▞▜▌▐▌ ▐▌▐▌  █▐▌ ▐▌  █  ▐▌  █    ▐▌     █ ▐▌ ▐▌▐▌ ▐▌▐▌   ")
        print("\t\t\t▐▌  ▐▌▐▛▀▜▌▐▌  █▐▛▀▚▖  █  ▐▌  █     ▝▀▚▖  █ ▐▛▀▜▌▐▛▀▚▖ ▝▀▚▖")
        print("\t\t\t▐▌  ▐▌▐▌ ▐▌▐▙▄▄▀▐▌ ▐▌▗▄█▄▖▐▙▄▄▀    ▗▄▄▞▘  █ ▐▌ ▐▌▐▌ ▐▌▗▄▄▞▘")
        print("------------------------------------------------------------------------------------------------------------")
        
        clave_encriptacion = Encriptar.generador_clave()
        Base_datos.guardar_json_clave(clave_encriptacion)

        if not Base_datos.comprobar_fichero_encriptado() or Base_datos.comprobar_fichero_vacio():
            Base_datos.encriptar_fichero()
    
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

            if len(contraseña)<8 or contraseña.isalpha() or contraseña.isdigit() or contraseña.isalnum() or contraseña.islower():
                print("\n-----La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un caracter especial, inténtelo de nuevo-----")
        
            else:
                contraseña_adecuada = True
        
        confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")

        while contraseña != confirmar_contraseña:
            print("\n-------------------------Las contraseñas no coinciden, por favor, vuelva a intentarlo-------------------------")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")
            confirmar_contraseña = getpass.getpass("\nConfirme la contraseña: ")
        
        salt = Encriptar.generador_salt(usuario)
        token = Encriptar.generador_token(usuario, contraseña.encode(), salt)

        Base_datos.desencriptar_fichero()

        Base_datos.guardar_json_salt_token(usuario, salt, token)
        
        Base_datos.crear_carpeta_usuario(usuario)

        Base_datos.encriptar_fichero()

        print("\n----------------------------------------Usuario registrado con éxito----------------------------------------")

    def iniciar_sesion(self):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tINICIO DE SESIÓN \n------------------------------------------------------------------------------------------------------------")
        inicio_correcto = False
        while not inicio_correcto:
            usuario = input("\nIngrese el nombre de usuario: ")
            contraseña = getpass.getpass("\nIngrese la contraseña: ")

            Base_datos.desencriptar_fichero()
            if Base_datos.confirmar_usuario(usuario):
                salt_guardado = Base_datos.sacar_json_salt(usuario)
                token_nuevo = Encriptar.generador_token(usuario, contraseña.encode(), salt_guardado)
                token_guardado = Base_datos.sacar_json_token(usuario)
                Base_datos.encriptar_fichero()

                if token_nuevo.hex() == token_guardado:
                    self.seguir_en_inicio = False
                    inicio_correcto = True
                    self.juego(usuario)

                else:
                    print("\n-----------------------------Usuario o contraseña incorrectos, inténtelo de nuevo-----------------------------")

            else:
                print("\n-----------------El usuario no existe en nuestra base de datos o la contraseña es incorrecta-----------------")
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
        clave = Encriptar.generador_clave_chacha20_poly()
        num_unico = os.urandom(12)

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
            print("\n------------------------------------------------------------------------------------------------------------")
            
            pregunta_compra = "\n¿DESEA COMPRAR ALGÚN JUGADOR? (si/no): "
            pregunta_compra_cifrada = Encriptar.encriptar_mensaje(clave, pregunta_compra, num_unico)
            print("\nPregunta de compra cifrada: ", pregunta_compra_cifrada)

            try:
                pregunta_compra_descifrada = Encriptar.desencriptar_mensaje(clave, pregunta_compra_cifrada, num_unico)
                print("\nPregunta de compra descifrada: ", pregunta_compra_descifrada)
            except:
                print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")
                
            print("\n------------------------------------------------------------------------------------------------------------")

            respuesta_texto = input(pregunta_compra_descifrada).lower()
            
            respuesta_compra_cifrada = Encriptar.encriptar_mensaje(clave, respuesta_texto, num_unico)
            print("\nRespuesta de la compra cifrada: ", respuesta_compra_cifrada)

            try:
                respuesta_compra_descifrada = Encriptar.desencriptar_mensaje(clave, respuesta_compra_cifrada, num_unico)
                print("\nRespuesta de la compra descifrada: ", respuesta_compra_descifrada)

                if respuesta_compra_descifrada == "si":
                    self.comprar_jugador(usuario, jugadores_aleatorios, precios_jugadores)
                    acabar_pregunta = True

                elif respuesta_compra_descifrada == "no":
                    print("\n---------------------------------------No ha comprado ningún jugador---------------------------------------")
                    acabar_pregunta = True
                
                else:
                    print("\n---------------------------------------------Comando no válido---------------------------------------------")
                    
                    respuesta_texto = input("\nPor favor, ingrese 'si' o 'no': ").lower()
                    respuesta_compra_cifrada = Encriptar.encriptar_mensaje(clave, respuesta_texto, num_unico)
                    print("\nRespuesta de la compra cifrada: ", respuesta_compra_cifrada)

                    try:
                        respuesta_compra_descifrada = Encriptar.desencriptar_mensaje(clave, respuesta_compra_cifrada, num_unico)
                        print("\nRespuesta de la compra descifrada: ", respuesta_compra_descifrada)

                        if respuesta_compra_descifrada == "si":
                            self.comprar_jugador(usuario, jugadores_aleatorios, precios_jugadores)
                            acabar_pregunta = True

                        elif respuesta_compra_descifrada == "no":
                            print("\n---------------------------------------No ha comprado ningún jugador---------------------------------------")
                            acabar_pregunta = True
                    
                    except:
                        print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")
            except:
                print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")

        
    def comprar_jugador(self, usuario, jugadores_aleatorios, precios_jugadores):
        print("\n-----------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tCOMPRAR JUGADOR \n-----------------------------------------------------------------------------------------------------------")

        clave = Encriptar.generador_clave_chacha20_poly()
        num_unico = os.urandom(12)

        print("\n------------------------------------------------------------------------------------------------------------")
        pregunta_jugador = "\nIngrese el nombre del jugador que desea comprar: "
        pregunta_jugador_cifrada = Encriptar.encriptar_mensaje(clave, pregunta_jugador, num_unico)
        print("\nPregunta del jugador cifrada: ", pregunta_jugador_cifrada)

        try:
            pregunta_jugador_descifrada = Encriptar.desencriptar_mensaje(clave, pregunta_jugador_cifrada, num_unico)
            print("\nPregunta del jugador descifrada: ", pregunta_jugador_descifrada)
        except:
            print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")
        print("\n------------------------------------------------------------------------------------------------------------") 
        
        jugador_comprado = input(pregunta_jugador_descifrada)
        respuesta_jugador_cifrada = Encriptar.encriptar_mensaje(clave, jugador_comprado, num_unico)
        print("\nRespuesta del jugador cifrada: ", respuesta_jugador_cifrada)

        try:
            respuesta_jugador_descifrada = Encriptar.desencriptar_mensaje(clave, respuesta_jugador_cifrada, num_unico)
            print("\nRespuesta del jugador descifrada: ", respuesta_jugador_descifrada)
            compra_de_jugadores = True
            while compra_de_jugadores:
                if jugador_comprado in jugadores_aleatorios:
                    precio_jugador = precios_jugadores[jugador_comprado]
                    Base_datos.fichar_jugador(usuario, jugador_comprado, precio_jugador)
                    compra_de_jugadores = False
                else:
                    print("\n------------------------------------Jugador no disponible en el mercado------------------------------------")
                    jugador_comprado = input("\nIngrese el nombre del jugador que desea comprar: ")
                    respuesta_jugador_cifrada = Encriptar.encriptar_mensaje(clave, jugador_comprado, num_unico)
                    print("\nRespuesta del jugador cifrada: ", respuesta_jugador_cifrada)
                    try:
                        respuesta_jugador_descifrada = Encriptar.desencriptar_mensaje(clave, respuesta_jugador_cifrada, num_unico)
                        print("\nRespuesta del jugador descifrada: ", respuesta_jugador_descifrada)
                    except:
                        print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")
        except:
            print ("\n--------------------------Ha habido un error en la autenticación del mensaje--------------------------")
    
    def equipo(self, usuario):
        print("\n------------------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tTU EQUIPO \n------------------------------------------------------------------------------------------------------------")
        print("\nJUGADORES DE TU EQUIPO: \n")
        Base_datos.visualizar_equipo(usuario)
        print("\n------------------------------------------------------------------------------------------------------------")
        