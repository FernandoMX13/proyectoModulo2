#!/usr/bin/env python3

import socket
import threading
import time
  
def points():
    time.sleep(2)
    print(". ", end = '', flush=True)
    
def connectionImport():
    HOST = "0.0.0.0"
    PORT = 1331

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Esperando conexiones.", end = '', flush=True)
        s.bind((HOST, PORT))
        t1 = threading.Thread(target=points)  
        t1.start()
        s.listen()
        t1.stop()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                size = conn.recv(1024)
                print(size)
                data = conn.recv(size)
                nombre = conn.recv(1024)
                print(data)
                f = open('/etc/apache2/sites-available/'+ nombre, 'w+b')
                binary_format = bytearray(byte_arr)
                f.write(binary_format)
                f.close()

#def installPre():
    #subprocess.Popen(['apt-get','install', 'apache2'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()


#installPre()
connectionImport()