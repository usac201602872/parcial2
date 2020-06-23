#Importacion de librerias
import logging
import socket
import sys
import os
import paho.mqtt.client as paho

SERVER_IP = '' #Colocar en el medio de las comillas la ip a utilizar
SERVER_PORT = 9814
BUFFER_SIZE = 64 * 1024

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