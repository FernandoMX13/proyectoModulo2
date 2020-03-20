import socket
import time

IP="192.168.216.145"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
print("Esperando conexion para mandar archivo", end = '', flush=True)
while not connected:
	try:
		time.sleep(1)
		s.connect((IP,1331))
		connected = True
	except Exception as e:
		print(". ", end = '', flush=True)
		print ("I/O error({0}): {1}".format(e.errno, e.strerror))
s.sendall(bytes("abcdefg", 'UTF-8'))
data = s.recv(1024)
print ("\n\nRespuesta: " + data.decode("utf-8"))
