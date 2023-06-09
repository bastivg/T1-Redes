# socket: La libreria a utilizar

import socket

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


# definicion de host y puerto: Indicarán hacia donde nos estaremos conectando inicialmente
host = 'jdiaz.inf.santiago.usm.cl'
port = 50006

# Un ejemplo en UDP
# Paso 1 - Definir el socket: el segundo argumento permite definir el tipo de conexión
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Paso 2 - Definir el mensaje a enviar: Debemos establecer un mensaje a enviar al servidor, recuerde codificarlo
msj = "GET NEW IMG DATA".encode()

# Paso 3 - Enviar el mensaje: Teniendo el mensaje y el socket basta con enviar el mensaje deseado
# se adjunta a la funcion el mensaje y una tupla con el host y puerto a comunicar
s.sendto(msj, (host, port))

# Paso 4 - Obtener la respuesta: Enviado el mensaje quead recibir la respuesta desde el servidor, siendo una lista con información,
# aunque solo usaremos el primer dato que se obtiene que contiene el mensaje que llega de vuelta, recordar decodificarlo.
# el valor dentro de recvfrom es el buffer que va a leer de lo recibido.
respuesta = s.recvfrom(1024)[0].decode()
print(respuesta)
elementos = respuesta.split()

diccionario = {}
for elemento in elementos:
    clave, valor = elemento.split(":")
    diccionario[clave] = int(valor)
    
buffer = diccionario["W"] * diccionario["H"] * 3

contador = 2
if "P3UDP" in diccionario:
    contador = 3
if "P3TCP" in diccionario:
    contador = 3
   
div_buffer = int(buffer/contador)



# Ejemplo para sacar y leer bytes de una foto
'''
Es el clásico de ejemplo de abrir y cerrar un archivo, solo que en vez de leer o escribir realizarlo con el comando read bytes y write bytes

open("nombre.txt", "w") -> open("nombre.txt", "wb") 

'''

## NOTA: Mucho ojo con lo que hace encode y decode, recuerden que la codificación con .encode() transforma un texto a bytes. [para cuando escriban la foto por ejemplo]
print(respuesta)

#s.close()  #cierro el socket para intentar abrirlo dnv
#Llamada por TCP

port = diccionario["P1TCP"]
s_tcp_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tcp_1.connect((host,port))
print("a")
message = ("GET 1/" + str(contador) + " IMG ID:" + str(diccionario["ID"])).encode('utf-8')
s_tcp_1.sendto(message, (host, port))
print("b")
respuesta1 = s_tcp_1.recvfrom(div_buffer)[0]
print("obtuve la parte 1")
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




port = diccionario["P2UDP"]

# Un ejemplo en UDP
# Paso 1 - Definir el socket: el segundo argumento permite definir el tipo de conexión
s_udp_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Paso 2 - Definir el mensaje a enviar: Debemos establecer un mensaje a enviar al servidor, recuerde codificarlo
msj1 = ("GET 2/" + str(contador) + " IMG ID:" + str(diccionario["ID"])).encode()

msj2 = "GET 2/" + str(contador) + " IMG ID: " + str(diccionario["ID"])

print(msj2)

#Enviar el mensaje
s_udp_2.sendto(msj1, (host, port))
#Recibe el mensaje
respuesta2 = s_udp_2.recvfrom(div_buffer)[0]





#cambie buffer y [0].decode



