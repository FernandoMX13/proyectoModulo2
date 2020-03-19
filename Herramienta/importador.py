#!/usr/bin/env python3

import os
import subprocess
import socket
import threading
import time
import re
import sys
    
def importSiteConf():
    print("Esperando importacion de archivo", end = '', flush=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1331))
    s.listen(1)
    conn, addr = s.accept()

    nombre = conn.recv(1024)
    print("Nombre del sitio: " + nombre.decode("utf-8"))
    conn.sendall(bytes('Nombre recibido', 'UTF-8'))
    
    contenido = conn.recv(1000000)
    f = open(nombre.decode("utf-8"), 'w+b')
    f.write(contenido)
    f.close()
    conn.sendall(bytes('Archivo recibido', 'UTF-8'))

    responder = conn.recv(1024)
    print("Archivo creado.")
    conn.sendall(bytes('Archivo creado sitio1', 'UTF-8'))

    nombre2 = conn.recv(1024)
    print("Nombre del sitio: " + nombre2.decode("utf-8"))
    conn.sendall(bytes('Nombre recibido', 'UTF-8'))
    
    contenido = conn.recv(1000000)
    f = open(nombre2.decode("utf-8"), 'w+b')
    f.write(contenido)
    f.close()
    conn.sendall(bytes('Archivo recibido', 'UTF-8'))

    responder = conn.recv(1024)
    print("Archivo creado.")
    conn.sendall(bytes('Archivo creado sitio2', 'UTF-8'))
    conn.close()

    return nombre.decode("utf-8"),nombre2.decode("utf-8")

def installPre():
    print("Update")
    info = subprocess.Popen(['apt-get','update', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo hacer update")
    else:
        print("Se logro hacer update")
    print("Upgrade")
    info = subprocess.Popen(['apt-get','upgrade', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo hacer upgrade")
    else:
        print("Se logro hacer upgrade")
    print("Instalando/verificando apache")
    info = subprocess.Popen(['apt-get','install', 'apache2', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo instalar apache")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Apache instalado")
    print("Instalando/verificando php")
    info = subprocess.Popen(['apt-get', 'install', 'php7.3', 'libapache2-mod-php7.3', 'php7.3-cli', 'php7.3-pgsql', 'php7.3-intl', 
        'php7.3-mysql', 'php7.3-curl', 'php7.3-gd', 'php7.3-soap', 'php7.3-xml', 'php7.3-zip', 
        '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo instalar php verifique conexion")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Php instalado")
    print("Instalando git")
    info = subprocess.Popen(['apt-get','install','git','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar git")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Git instalado")
    print("Instalando/verificando drush")
    info = subprocess.Popen(['wget','https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar', '-q','--show-progress']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo descaragr drush")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drush descargado")
    info = subprocess.Popen(['chmod','+x','drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo cambiar permisos a drush")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Permisos asignados a drush")
    info = subprocess.Popen(['mv','drush.phar','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo agragar drush al path")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drush agregado al path")
    print("Instalando cliente de postgresql")
    info = subprocess.Popen(['apt-get','install','postgresql-client-11','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede instalar cliente de postgresql")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Cliente de postgresql instalado")
    print("Descargando Drupal")
    info = subprocess.Popen(['drush', 'dl', 'drupal-8.8.3', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se descarger drupal 8.8.3")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal descargado")

def installDrupal(nombreSitio):
    f = open(nombreSitio, "r")
    for linea in f:
        if linea.lower().find("documentroot") != -1:
            pat = re.compile(".*#.*documentroot.*")
            result = pat.match(linea.lower())
            if(result == None):
                s1 = linea.split()
                s = s1[1].split('#')
                cad = s[0].replace(' ','')
                break
    f.close()
    print("Moviendo Drupal al sitio")
    info = subprocess.Popen(['cp', '-r', 'drupal-8.8.3/', cad]).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo mover drupal")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal ha sido movido")
    """
    user = input("Ingrese el usuario de la base de datos.\n")
    ip = input("Direccion de la base de datos.\n")
    port = input("Puerto de la base de datos.\n")
    bd = input("Base de datos a la conectarse.\n")
    password = input("Ingrese la coontraseña de acceso.\n")
   """
    user='drupal'
    ip='192.168.216.148'
    port='5432'
    bd = user
    password = 'hola123.,'
    print("Relizando instalacion de drupal")
    url = "--db-url=pgsql://"+ user +":"+password+"@"+ip+":"+port+"/"+bd
    info = subprocess.Popen(['drush', 'si','standard',url, '-r', cad, '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    l = info.stdout.read().decode()
    l1 = l.find("Installation complete.")
    slicObj = slice(l1,l1+70)
    print(">> "+ l[slicObj])
    if l1 == -1:
        print("Problemas con la instalaciion")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Drupal instalado")

    s1 = nombreSitio.split('/')
    print("Activando sitio.")
    info = subprocess.Popen(['a2ensite', s1[-1]]).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo activar la pagina")
        print("Abortando operacion")
        sys.exit()
    info = subprocess.Popen(['a2enmod', 'rewrite']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error de activacion del sitio")
        sys.exit()
    print("Reiniciando pagina.")
    info = subprocess.Popen(['/etc/init.d/apache2', 'restart']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error Reiniciando apache")
        sys.exit()
def deleteDL():
    print("Eliminando descargable")
    info = subprocess.Popen(['rm', '-r', 'drupal-8.8.3', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Problemas al quitar el descargable")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Descargable eliminado")
installPre()
nombreSitio1, nombreSitio2 = importSiteConf()
print(nombreSitio1)
print(nombreSitio2)
sys.exit()
installDrupal(nombreSitio1)
#installDrupal(nombreSitio2)
deleteDL()