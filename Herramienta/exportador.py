#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import asyncio
import socket
import re
import time

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

def comunicandoConImportador(IP, DOC):
	PORT = 1331
	PATH = "/etc/apache2/sites-available/" + DOC
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		connected = False
		print("Esperando conexion con el servidor ", end = '', flush=True)
		while not connected:
			try:
				time.sleep(2)
				s.connect((IP,PORT))
				connected = True
			except Exception as e:
				print(". ", end = '', flush=True)

		bin_data = open(PATH, 'rb')
		s.sendall(bin_data.len)
		s.sendall(bin_data)
		s.sendall(DOC)
		data = s.recv(1024)

verificandoDrush()
verificandoGit()
"""
flag = False
toInstall = subprocess.Popen(['drush', 'pm-list', '--status=Enabled', '--fields=name', '-r', '/var/www/drupal'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
s1 = toInstall.stdout.read().decode().split('(') 
for s in s1:
	cad = s.split(')')
	if (flag):
		print(">"+cad[0]+"<")
	flag = True
"""
pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
IP = input('Ingrese la ip del host:\n')
result = pat.match(IP)
while result == None:
	IP = input('[!] Ingrese una ip correcta:\n')
	result = pat.match(IP)
IP = "192.168.216.145"
DOC = 'drupal.con'
while(os.path.isfile("/etc/apache2/sites-available/"+DOC)):
    DOC = input("Ingrese solo el nombre del archivo de configuracion del sitio (Ubicado en /etc/apache2/sites-available/)\n")
comunicandoConImportador(IP, DOC)
