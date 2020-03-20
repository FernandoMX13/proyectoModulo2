#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import re
import time
import struct
import datetime 

def backUP(DOC,sitio):
	s1 = ""
	f = open(DOC, "r")
	for linea in f:
	    if linea.lower().find("documentroot") != -1:
	        pat = re.compile(".*#.*documentroot.*")
	        result = pat.match(linea.lower())
	        if(result == None):
	            l1 = linea.split()
	            for j in l1[1:]:
	                s1+=j+' '
	            s = s1.split('#')
	            cad = s[0].rstrip().lstrip()
	            break
	f.close()
	dateTimeObj = datetime.datetime.now()
	timestampStr = dateTimeObj.strftime("%H_%M_%S_%f-%d-%b-%Y.tar.gz")
	subprocess.Popen(['drush', 'archive-dump', '--destination=/var/www/bck'+sitio+timestampStr,'-r',cad]).wait()
	print("Respaldo Creado")

def downloadDrush(type):
	if(type):
		comands = ["/usr/local/sbin/drush","/usr/local/bin/drush",
		"/usr/sbin/drush", "/usr/bin/drush","/sbin/drush","/bin/drush"]
		for c in comands :
			subprocess.Popen(['rm',c],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
		subprocess.Popen(['apt-get','purge','drush','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['wget','https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['chmod','+x','drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['mv','drush.phar','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

def verificandoDrush():
	try:
		drush = subprocess.Popen(['drush','--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		version = drush.stdout.read().decode().find('8.3.2')
		if (version == -1 ):
			print("Actualizando drush")
			downloadDrush(True)
	except FileNotFoundError:
		print("Instalando drush")
		downloadDrush(False)
	print("Drush instalado/actualizado")
	

def verificandoGit():
	try:
		git = subprocess.Popen(['git'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		print("Instalando git")
		subprocess.Popen(['apt-get','install','git'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	print("Git instalado")	

def exportSiteConfig(IP,DOC,DOC2):
	f = open (DOC, "rb")
	l = f.read(1000000)
	f2 = open (DOC2, "rb")
	l2 = f2.read(1000000)
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
	s.sendall(bytes(DOC, 'UTF-8'))
	data = s.recv(1024)
	print ("\n\nRespuesta: " + data.decode("utf-8"))

	s.sendall(l)
	data = s.recv(1024)
	print ("Respuesta: " + data.decode("utf-8"))

	s.sendall(bytes(' ', 'UTF-8'))
	data = s.recv(1024)
	print ("Respuesta: " + data.decode("utf-8"))

	s.sendall(bytes(DOC2, 'UTF-8'))
	data = s.recv(1024)
	print ("\n\nRespuesta: " + data.decode("utf-8"))

	s.sendall(l2)
	data = s.recv(1024)
	print ("Respuesta: " + data.decode("utf-8"))

	s.sendall(bytes(' ', 'UTF-8'))
	data = s.recv(1024)
	print ("Respuesta: " + data.decode("utf-8"))
	f.close()
	f2.close()
	s.close()

verificandoDrush()
verificandoGit()
"""
flag = False
pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
IP = input('Ingrese la ip del host:\n')
result = pat.match(IP)
while result == None:
	IP = input('[!] Ingrese una ip correcta:\n')
	result = pat.match(IP)

DOC = input('Ingrese la ruta absoluta del archivo de configuración del sitio1\n')
while(os.path.isfile("DOC) == False):
    DOC = input("[!] Ingresa la ruta completa del archivo de configuración.\n")

DOC2 = input('Ingrese la ruta absoluta del archivo de configuración del sitio1\n')
while(os.path.isfile("DOC2) == False):
    DOC2 = input("[!] Ingresa la ruta completa del archivo de configuración.\n")
"""
IP = "192.168.216.145"
DOC = '/etc/apache2/sites-available/drupal.conf'
DOC2 = '/etc/apache2/sites-available/drupal2.conf'
backUP(DOC,"sitio1")
#backUP(DOC2,"sitio2")
exportSiteConfig(IP,DOC,DOC2)
print("\nSe termino de enviar los archivos de configuracion.")