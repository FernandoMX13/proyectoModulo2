import socket

print("Esperando importacion de archivo")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 1331))
s.listen()
conn, addr = s.accept()
nombre = conn.recv(1024)
print("Recived: " + nombre.decode("utf-8"))
conn.sendall(bytes("Echo: "+ nombre.decode("utf-8"), 'UTF-8'))
