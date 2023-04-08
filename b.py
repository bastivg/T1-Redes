# socket: La libreria a utilizar
import socket

#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)


# definicion de host y puerto: Indicarán hacia donde nos estaremos conectando inicialmente
host = 'jdiaz.inf.santiago.usm.cl'
port = 50006

# Un ejemplo en UDP
def llamado_1_udp(host_udp,port_udp):
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Mensaje enviado a : <",port,"> por <UDP>: <GET NEW IMG DATA>")
    msj = "GET NEW IMG DATA".encode()
    s_udp.sendto(msj, (host_udp, port_udp))
    respuesta = s_udp.recvfrom(1024)[0].decode()
    print("Mensaje recibido de: <", port,"> por <UDP>: <",respuesta,">")
    return respuesta

def llamado_tcp(host_tcp,port_tcp,n): #n = n / 3
    s_tcp_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp_1.connect((host_tcp,port_tcp))
    msj_pt1 = ("GET " + str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"]))
    print("Mensaje enviado a ", diccionario["ID"], ": <", port_tcp,"> por <TCP>: <", msj_pt1, ">")
    
    msj_pt1 = ("GET " + str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"])).encode('utf-8')
    s_tcp_1.sendto(msj_pt1, (host_tcp, port_tcp))
    respuesta_tcp = s_tcp_1.recvfrom(div_buffer)[0]
    print("Mensaje recibido de: <", diccionario["ID"], ">:<", port_tcp,"> por <TCP>: <Se reciben los bytes de pt.",n,">")
    return respuesta_tcp

def llamado_2_udp(host_udp,port_udp,n):
    s_udp_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msj_pt2 = ("GET "+ str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"]))
    print("Mensaje enviado a ", diccionario["ID"], ": <", port_udp,"> por <UDP>: <", msj_pt2, ">")
    msj_pt2 = ("GET "+ str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"])).encode()
    s_udp_2.sendto(msj_pt2, (host_udp, port_udp))
    respuesta_pt2 = s_udp_2.recvfrom(div_buffer)[0]
    print("Mensaje recibido de: <", diccionario["ID"], ">:<", port_udp,"> por <UDP>: <Se reciben los bytes de pt.",n,">")
    return respuesta_pt2

def verificador(vef_b):
    s_tcp_pv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp_pv.connect((host,diccionario["PV"]))
    msj_pv = vef_b
    s_tcp_pv.sendto(msj_pv, (host, diccionario["PV"]))
    respuesta_pv = s_tcp_pv.recvfrom(div_buffer)[0].decode()
    print(respuesta_pv)
    if "200" in respuesta_pv:
        print("entro al success")
        return 0
    return 1





respuesta1 = llamado_1_udp(host,port)
elementos = respuesta1.split()
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





#Llamada por TCP

respuesta_pt1 = llamado_tcp(host,diccionario["P1TCP"],1)

#Llamada por UDP

respuesta_pt2 = llamado_2_udp(host,diccionario["P2UDP"],2)

if "P3UDP" in diccionario:
    respuesta_pt3 = llamado_2_udp(host,diccionario["P3UDP"],3)
    i = verificador(respuesta_pt1+respuesta_pt2+respuesta_pt3)
    print("probando verificador:", i)
    f = open("itento.png", "wb")
    f.write(respuesta_pt1)
    f.write(respuesta_pt2)
    f.write(respuesta_pt3)
    f.close()
elif "P3TCP" in diccionario:
    respuesta_pt3 = llamado_tcp(host,diccionario["P3TCP"],3)
    f = open("itento.png", "wb")
    f.write(respuesta_pt1)
    f.write(respuesta_pt2)
    f.write(respuesta_pt3)
    f.close()
else :
    i = verificador(respuesta_pt1+respuesta_pt2)
    print("probando verificador: 0 = success ", i)
    f = open("itento.png", "wb")
    f.write(respuesta_pt1)
    f.write(respuesta_pt2)
    f.close()
