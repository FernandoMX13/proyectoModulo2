#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import re
import time
import struct
import datetime
import subprocess
import threading
import sys

configuracionsitio1 = "/etc/apache2/sites-available/drupal.conf"
configuracionsitio2 = "/etc/apache2/sites-available/drupal2.conf"
ubicacionHtaccessSitio1 = "/var/www/drupal/.htaccess"
ubicacionHtaccessSitio2 = "/var/www/drupal2/.htaccess"
confifuracionApache = "/etc/apache2/apache2.conf"
ipServidorNuevo = "192.168.216.145"

def backUP(DOC,sitio):
	print("\t[-] Creando respaldo del " + sitio)
	t = threading.Thread(target=spin)
	t.start()
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
	t.do_run = False
	t.join()
	print("\t[*] Respaldo para el " + sitio + " creado.")

def downloadDrush(type):
	t = threading.Thread(target=spin)
	t.start()
	if(type):
		comands = ["/usr/local/sbin/drush","/usr/local/bin/drush",
		"/usr/sbin/drush", "/usr/bin/drush","/sbin/drush","/bin/drush"]
		for c in comands :
			subprocess.Popen(['rm',c],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
		subprocess.Popen(['apt-get','purge','drush','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['wget','https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['chmod','+x','drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	subprocess.Popen(['mv','drush.phar','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	t.do_run = False
	t.join()

def verificandoDrush():
	try:
		drush = subprocess.Popen(['drush','--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		version = drush.stdout.read().decode().find('8.3.2')
		if (version == -1 ):
			print("\t[-] Actualizando drush")
			downloadDrush(True)
	except FileNotFoundError:
		print("\t[-] Instalando drush")
		downloadDrush(False)
	print("\t[*] Drush esta instalado yactualizado")

def verificandoGit():
	try:
		git = subprocess.Popen(['git'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		print("Instalando git")
		subprocess.Popen(['apt-get','install','git', '-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	print("Git instalado")	

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def spin():
    t = threading.currentThread()
    spinner = spinning_cursor()
    while getattr(t, "do_run", True):
        print(next(spinner),end = '')
        sys.stdout.flush()
        time.sleep(0.1)
        print('\b',end = '')

def exportSiteConfig():
	print("\t[-]Obteniendo y comprimiendo archivos.")
	t = threading.Thread(target=spin)
	t.start()

	cmd = "mkdir .tmp"
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "cp {0} .tmp/sitio1.conf".format(configuracionsitio1)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "cp {0} .tmp/sitio2.conf".format(configuracionsitio3)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "cp {0} .tmp/htaccess1".format(ubicacionHtaccessSitio1)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "cp {0} .tmp/htaccess2".format(ubicacionHtaccessSitio2)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "cp {0} .tmp/configuracion".format(confifuracionApache)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "echo '{0}\n{1}\n{2}\n{3}\n{4}\n' > .tmp/ubicaciones"\
	.format(configuracionsitio1,configuracionsitio3,ubicacionHtaccessSitio1,ubicacionHtaccessSitio2,confifuracionApache)
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "tar -czvf .archivosConfiguracion.tar.gz .tmp/"
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	t.do_run = False
	print("\t[*]Archivos comprimidos.\n\t[-]Mandando archivos al " + ipServidorNuevo)

	cmd = "scp -P 1331 .archivosConfiguracion.tar.gz root@{0}:/tmp/archivosConfiguracion.tar.gz".format(ipServidorNuevo)
	info = subprocess.Popen(cmd, shell=True).wait()

	cmd = "rm -r .tmp"
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

	cmd = "rm .archivosConfiguracion.tar.gz"
	info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
	print("\t[*] Archivos enviados.")

flag = False
result = pat.match(ipServidorNuevo)
if result == None:
	print('\t[!] La direccion IP es invalida.\n')
	flag = True
DOC = configuracionsitio1
if os.path.isfile(DOC) == False:
    print("\t[!] La ruta para el archivo de configuracion del sitio1 no es valida o no se encuentra\n")
    flag = True
DOC2 = configuracionsitio1
if os.path.isfile(DOC2) == False:
    print("\t[!] La ruta para el archivo de configuracion del sitio2 no es valida o no se encuentra\n")
    flag = True
if os.path.isfile(ubicacionHtaccessSitio1) == False:
    print("\t[!] La ruta para el archivo .htaccess del sitio1 no es valida o no se encuentra\n")
    flag = True
if os.path.isfile(ubicacionHtaccessSitio2) == False:
    print("\t[!] La ruta para no el archivo .htaccess del sitio2 no es valida o no se encuentra\n")
    flag = True
if os.path.isfile(confifuracionApache) == False:
    print("\t[!] La ruta para el archivo de configuracion de apache no es valida o no se encuentra\n")
    flag = True
if flag :
	sys.exit()
verificandoDrush()
verificandoGit()
backUP(DOC,"sitio 1")
backUP(DOC2,"sitio 2")
exportSiteConfig()
print("\t [*] Se termino de enviar los archivos de configuracion.De manera exitosa puede continuar con el proceso en el nuevo servidor.")
