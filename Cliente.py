#Importacion de librerias
import logging
import socket
import sys
import os
import paho.mqtt.client as paho
import threading
import time
import datetime
import binascii

SERVER_IP = '' #Colocar en el medio de las comillas la ip a utilizar
SERVER_PORT = 9817 #Puerto del Socket a utilizar
BUFFER_SIZE = 64 * 1024 #Buffer de 64 KB

# Credenciales de MQTT
MQTT_HOST = '167.71.243.238'
MQTT_PORT = '1883'
MQTT_USER = 'proyectos'
MQTT_PASS = 'proyectos980'

#Cliente de MQTT
client = paho.Client(clean_session=True)
client.username_pw_set(MQTT_USER,MQTT_PASS)
client.connect(host=MQTT_HOST, port=MQTT_PORT)

Separador = '/'
Sala = 'S17'
ID = '202058457'
Peso = '5741'

topic = Sala + Separador + ID + Separador + Peso


while True:
    
    # Se crea socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Se conecta al puerto donde el servidor se encuentra a la escucha
    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)
    print('Conectando a {} en el puerto {}'.format(*server_address))
    Reciviendo = input('Comando: ' )

    try:

        # Se envia un texto codificado EN BINARIO
        message = Reciviendo.encode()
        print(type(message))#Imprime el mensaje que ha recibido del encode
        print('\n\nEnviando texto:  {!s}'.format(message)) #Se envia un mensaje
        sock.sendall(message) #Se envia utilizando "socket.sendall" 

#Inicia con la grabacion
        logging.info('Comenzando grabacion')
        os.system('arecord -d 10 -f U8 -r 8000 audio.mp3')

        f = open ("audio.mp3", "rb")
        l = f.read(BUFFER_SIZE)
        while (l):
            sock.sendall(l)
            l = f.read(BUFFER_SIZE)
            print('Enviando...')
        f.close()
        print('Salio')
        
        # Esperamos la respuesta del ping servidor
        bytesR = 0  #Bit a ser Recividos
        bytesE = len(message) #Bits a ser enviados

    finally:
        print('\n\nConexion finalizada con el servidor')
        sock.close()