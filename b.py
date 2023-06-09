# socket: La libreria a utilizar
import socket


# definicion de host y puerto: Indicarán hacia donde nos estaremos conectando inicialmente
host = 'jdiaz.inf.santiago.usm.cl'
port = 50006


# Para la primera llamada por udp, obteniendo la Id, anchos y largos...
# Recibe el host y el puerto por el cual se realiza la primera llamada.
def llamado_1_udp(host_udp,port_udp):
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Mensaje enviado a : <",port,"> por <UDP>: <GET NEW IMG DATA>")
    msj = "GET NEW IMG DATA".encode()
    s_udp.sendto(msj, (host_udp, port_udp))
    respuesta = s_udp.recvfrom(1024)[0].decode()
    print("Mensaje recibido de: <", port,"> por <UDP>: <",respuesta,">")
    return respuesta

# Hace una llamada TCP, recibe el host de tcp, el port, y n que es la parte de la imagen.
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

# Hace un llamado UDP, recibe el host de udp, el port, y n que es la parte de la imagen.
def llamado_2_udp(host_udp,port_udp,n):
    s_udp_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msj_pt2 = ("GET "+ str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"]))
    print("Mensaje enviado a ", diccionario["ID"], ": <", port_udp,"> por <UDP>: <", msj_pt2, ">")
    msj_pt2 = ("GET "+ str(n) + "/" + str(contador) + " IMG ID:" + str(diccionario["ID"])).encode()
    s_udp_2.sendto(msj_pt2, (host_udp, port_udp))
    respuesta_pt2 = s_udp_2.recvfrom(div_buffer)[0]
    print("Mensaje recibido de: <", diccionario["ID"], ">:<", port_udp,"> por <UDP>: <Se reciben los bytes de pt.",n,">")
    return respuesta_pt2

# Se conecta con el canal para verificar, que la imagen tenga los bits correctos.
# Recibe los bits a verificar
def verificador(vef_b):
    print("verificando respuesta... este proceso puede tardar")
    s_tcp_pv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp_pv.connect((host,diccionario["PV"]))
    msj_pv = vef_b
    s_tcp_pv.sendto(msj_pv, (host, diccionario["PV"]))
    respuesta_pv = s_tcp_pv.recvfrom(div_buffer)[0].decode()
    print("Se obtuvo respuesta!!!: ",respuesta_pv)
    if "200" in respuesta_pv:
        return 0
    print("El proceso fallo uwu")
    return 1

# Va a crear la imagen, recibiendo la respuesta 1, 2, 3 y n que son las partes que tiene la imagen
def creacion_img(rp1,rp2,rp3,n):
    if n == 2:
        i = verificador(rp1+rp2)
        if i == 0:
            print("Creando imagen")
            print("Pintando la imagen")
            f = open(str(diccionario["ID"]) + "Imagen.png", "wb")
            f.write(rp1)
            f.write(rp2)
            f.close()
            print("Imagen lista")
            return False
        else:
            return True
            
    else:
        i = verificador(rp1+rp2+rp3)
        if i == 0:
            print("Creando imagen")
            print("Pintando la imagen")
            f = open(str(diccionario["ID"]) + "Imagen.png", "wb")
            f.write(rp1)
            f.write(rp2)
            f.write(rp3)
            f.close()
            print("Imagen lista")
            return False
        else:
            return True



veff = True   # veff va a generar el bucle esperando a recibir la imagen de forma correcta.

while veff:
    print("Iniciando un nuevo Proceso \n>:D\n")
    respuesta1 = llamado_1_udp(host,port)
    elementos = respuesta1.split()
    diccionario = {}
    for elemento in elementos:
        clave, valor = elemento.split(":")
        diccionario[clave] = int(valor)  # Creo un diccionario con cada propiedad que retorna la primera llamada
        
    buffer = diccionario["W"] * diccionario["H"] * 3 # Calculo el buffer

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

    #Llamada 3:
    if "P3UDP" in diccionario:
        respuesta_pt3 = llamado_2_udp(host,diccionario["P3UDP"],3)
        veff = creacion_img(respuesta_pt1,respuesta_pt2,respuesta_pt3,3)
    elif "P3TCP" in diccionario:
        respuesta_pt3 = llamado_tcp(host,diccionario["P3TCP"],3)
        veff = creacion_img(respuesta_pt1,respuesta_pt2,respuesta_pt3,3)
    else:
        veff = creacion_img(respuesta_pt1,respuesta_pt2,"",2)
