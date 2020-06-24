import paho.mqtt.client as mqtt #importamos libreria de mqtt paho
import logging #Loggin Reemplaza al print
import time  
import os   #Para acceder al audio
import threading  #Para los hilo
import sys  
import binascii
import datetime

class Desicion(object):                     # Clase de desicion para obtener mas facil el topic
    def __init__(self,entrada,grupo,id):    # Los valores del topic en string
        self.entrada = entrada
        self.grupo = grupo
        self.id = id
    
    def getGrupo(self):         #Obtener el Grupo
        return self.grupo
    
    def getID(self):            #Obtener la ID (carnet o Sala)
        return self.id
    
    def getEntrada(self):       #Obtener el input(mensaje o audio)
        return self.entrada
    
    def modifyDesicion(self,NE,NG,NI): #Para poder modificar el topic
        self.entrada = NE
        self.grupo = NG
        self.id = NI

class ComandoInvalido(Exception): #Excepcion creada especificamente Por si un comando ingresado no es el correcto
    def __init__(self,comando):
        self.comando = comando
    
    def __str__(self):
        return str("Perdon, pero "+ str(self.comando)+" no es valido. Escriba las opciones que se les dieron.")

class Name(Exception):
    def __init__(self,name):
        self.name = name
    
    def __str__(self):
        return str("Feliz Dia")

# Credenciales para el archivo de audio
SERVER_IP = '' #Colocar en el medio de las comillas la ip a utilizar
SERVER_PORT = 9817 #Puerto del Socket a utilizar
BUFFER_SIZE = 64 * 1024 #Buffer de 64 KB

# Credenciales de MQTT
MQTT_HOST = "167.71.243.238"
MQTT_PORT =  1883        #numero de Puerto
MQTT_USER = "proyectos" #Nombre del usuario del MQTT
MQTT_PASS = "proyectos980"

#nombre = input("dime tu nombre: ")#con el input lo que hacemos es solicitar el nombre del participante
                                #se guarda en la variable nombre

def on_connect(client, userdata, flags, rc):#funcion que se ejecuta por la libreria MQTT
    logging.info("Conectado al broker")
    client.subscribe(topic) #topic donde se va a suscribir
    client.publish(topic) #enviamos un mensaje con el metodo "publish" con el topico raiz avisando que hemos ingresado
                                                             
def on_message(client, userdata, msg): #declaramos una funcion que sera ejecutada por la libreria MQTT cuando llegue un mensaje desde el servidor
    print(msg.payload.decode("utf-8"))#se imprime el mensaje que haya llegado
    msg.payload.decode("audio.wav")#se reproduce el mensaje que haya llegado
    os.system('aplay audio.wav')

print("Bienvenido al Chat hecho con MQTT."
    "\nPor favor, ingrese los siguientes datos")

#-------------------------------------------- Configuracion Inicial para conectarse al broker --------------------------------

cliente = mqtt.Client()#aca declaramos una instancia del cliente "MQTT"
cliente.on_connect = on_connect #le digo a la libreria que funcion tiene que ejecutar cuando se concrete la conexion
cliente.on_message = on_message #le digo a la libreria que funcion tiene que ejecutar ante la llegada de un mensaje
cliente.username_pw_set(MQTT_USER, MQTT_PASS) #Se establece el usuario y contrasenia
cliente.connect(host=MQTT_HOST, port=MQTT_PORT)
cliente.loop_start() #si esto no se ejecuta todo el tiempo no podemos recibir mensajes
#-------------------------------------------------------------------------------------------------------------------------------

def audio_thread(tiempo):  # Hilo solo de audio
    logging.info('Comenzando grabacion')
    os.system('arecord -d '+tiempo+' -f U8 -r 8000 audio.wav') # comando bah en la terminal para audio
    f = open ("audio.wav", "rb")    #Lo abre en bytes
    enviar_audio = f.read(BUFFER_SIZE) 
    cliente.publish(topic, enviar_audio) #Se publica el audio que se quiere enviar

try:
    e = input('Que tipo de mensaje quiere enviar(mensaje, audio):')
    g = input('Entre a que grupo quiere ir(solo el numero):')
    i = input('Entre a que usuario(carne o sala) quiere enviar:')
    Persona = Desicion(e,g,i) 
except KeyboardInterrupt:
    print('\n\nSe ha deconectado del servidor')

while True: #generacion de bucle infinito para ir solicitando al usuario que vaya ingresando los mensajes
    try: 
        # Credenciales para topics
        global topic
        separador = "/"
        Entrada = Persona.getEntrada()
        Grupo = Persona.getGrupo()
        ID = Persona.getID()
        topic = Entrada+separador+Grupo+separador+ID
        if Entrada == 'mensaje':
            a_enviar = input ("Escribe un mensaje ---> ")#Aca se solicita el mensaje
            a_enviar = ID + ": " + a_enviar #Se concatena y se incluye el nombre dentro del mensaje
            cliente.publish(topic, a_enviar) #Se publica el mensaje que se quiere enviar
            d = input("Quiere seguir enviando otro tipo de mensaje a un usuario diferente? [Y/N]:") #Para seguir usando el programa y cambiar el topic
            if d == "Y" or d == "y": # Para enviar a otro usuario
                ne = input('Que tipo de mensaje quiere enviar(mensaje, audio):')
                ng = input('Entre a que grupo quiere ir(solo el numero):')
                ni = input('Entre a que usuario(carne o sala) quiere enviar:')
                Persona.modifyDesicion(ne,ng,ni) #modifica el topic
            elif d == "N" or d == "n":
                    print ('Conexion con el servidor finalizada')
                    break
            else:
                raise ComandoInvalido(d) #Levanta excepcion si no colocaalguna de las opciones
            
        elif Entrada == 'audio':
            duracion = input("Cuanto tiempo, en s, quiere grabar? :")
            voice = threading.Thread(target=audio_thread, args=(duracion)) #El hilo del audio
            voice.start() # Para iniciar el hilo
            voice.join() # espera a que el hilo termine, sin este, solo con un time.sleep(1) para continuar con el programa.
            d = input("Quiere seguir enviando otro tipo de mensaje a un usuario diferente? [Y/N]:")
            if d == "Y" or d == "y": #Para enviar a otro usuario
                ne = input('Que tipo de mensaje quiere enviar(mensaje, audio):')
                ng = input('Entre a que grupo quiere ir(solo el numero):')
                ni = input('Entre a que usuario(carne o sala) quiere enviar:')
                Persona.modifyDesicion(ne,ng,ni) #modifica el topic
            elif d == "N" or d == "n": #Para salir de la aplicacion
                print ('Conexion con el servidor finalizada')
                break
            else:
                raise ComandoInvalido(d) #Levanta excepcion si no coloca alguna de las dos opciones
        else:
            raise ComandoInvalido(Entrada)
    except KeyboardInterrupt:
        print('\n\nSe ha deconectado del servidor')
        break