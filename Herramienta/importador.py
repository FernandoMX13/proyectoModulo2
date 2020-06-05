#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import threading
import time
import re
import sys

#Datos del sitio 1 antiguo
usuarioDeBaseDatos1='drup'
ipServidorBaseDatos1='192.168.216.148'
Puerto1='5432'
NombreDeBaseDatosSitio1 = 'drupdb'
contrasenaDeBaseDatos1 = 'Hola123.,'

#Datos del sitio 2 antiguo
usuarioDeBaseDatos2='drupOld'
ipServidorBaseDatos2='192.168.216.148'
Puerto2='5432'
NombreDeBaseDatosSitio2 = 'drupOld'
contrasenaDeBaseDatos2 = 'Hola123.,'

#Datos del sitio 1 NUEVO
usuarioDeBaseDatos1N='drup2'
ipServidorBaseDatos1N='192.168.216.148'
Puerto1N='5432'
NombreDeBaseDatosSitio1N = 'drupdb2'
contrasenaDeBaseDatos1N = 'Hola123.,'

#Datos del sitio 2 Nuevo
usuarioDeBaseDatos2N='drupNew'
ipServidorBaseDatos2N='192.168.216.148'
Puerto2N='5432'
NombreDeBaseDatosSitio2N = 'drupNew'
contrasenaDeBaseDatos2N = 'Hola123.,'

flag = True

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
    print(" ",end = '')
    
def onlypath (ubi):
    cad = ""
    cnt = 1
    var = line.split('/')
    for n in var:
        if cnt != len(var):
            cad+=n
            cad+='/'
            cnt+=1
    return cad
    
def importSiteConf():
    print("\t[--]Inicia con el proceso de importacion de archivos de configuracion.")
    print("\t[-]Instalando y configurando ssh")
    t = threading.Thread(target=spin)
    t.start()
    cmd = "apt-get install openssh-server -y"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

    cmd = "sed -i -e 's/#Port 22/Port 1331/' \
           -i -e 's/#AddressFamily any/AddressFamily inet/' \
           -i -e 's/#PasswordAuthentication yes/PasswordAuthentication yes/'\
           -i -e 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/'\
           /etc/ssh/sshd_config"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

    cmd = "/etc/init.d/ssh restart"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    print ("\t[*] Se termino de instalar y configurara ssh")
    print ("\t[-] Ejecute el archivo exportador.py en el servidor antiguo")
    res = input("\t[-] Todo salio bien? (Y/N)\n ")

    while res != 'Y' and res != 'y' and res != 'N' and res != 'n' :
    	res = input("\t[!] Por favor escriba una respuesta correcta.\n 	")

    if res == 'N' or res == 'n':
    	rollback()

    print("\t[*] Desinstalando ssh ya que no lo necesitamos.")
    t = threading.Thread(target=spin)
    t.start()
    t.do_run = True
    cmd = "apt-get purge openssh-server -y"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()	
    t.do_run = False
    t.join()

    print("\t[-] Moviendo archivos importdos.")
    t.start()
    t.do_run = True
    cmd = "tar -xzvf /tmp/archivosConfiguracion.tar.gz"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()	

    filepath = '.tmp/ubicaciones'
    with open(filepath) as fp:
       line = fp.readline()
       line = line[:-1]
       sitio1 = line
       dir = onlypath(line)
       info = subprocess.Popen(['mkdir','-p', dir],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       info = subprocess.Popen(['cp','.tmp/sitio1.conf', line],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

       line = fp.readline()
       line = line[:-1]
       sitio2 = line
       dir = onlypath(line)
       info = subprocess.Popen(['mkdir','-p', dir],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       info = subprocess.Popen(['cp','.tmp/sitio2.conf', line],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       
       line = fp.readline()
       line = line[:-1]
       dir = onlypath(line)
       info = subprocess.Popen(['mkdir','-p', dir],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       info = subprocess.Popen(['cp','.tmp/htaccess1', line],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

       line = fp.readline()
       line = line[:-1]
       dir = onlypath(line)
       info = subprocess.Popen(['mkdir','-p', dir],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       info = subprocess.Popen(['cp','.tmp/htaccess2', line],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()

       line = fp.readline()
       line = line[:-1]
       dir = onlypath(line)
       info = subprocess.Popen(['mkdir','-p', dir],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       info = subprocess.Popen(['cp','.tmp/configuracion', line],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
       fp.close()
    t.do_run = False
    t.join()
    print("\t[*] archivos movidos.")

    return sitio1, sitio2

def installPre():
    print("\t[--]Iniciando con proceso de Instalaciones previas.")
    print("\t[-] Realizando update del sistema.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','update', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo hacer update.")
    else:
        print("\t[*] Update Terminado.")

    print("\t[-] Realizando upgrade del sistema.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','upgrade', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo hacer upgrade.")
    else:
        print("\t[*] Upgrade terminado.")

    print("\t[+] Instalando/verificando apache.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','install', 'apache2', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo instalar apache.")
        rollback()
    else:
        print("\t[*] Apache instalado.")

    print("\t[-] Instalando/verificando php.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get', 'install', 'php', 'libapache2-mod-php', 'php-cli', 'php-pgsql', 'php-intl', 
        'php-mysql', 'php-curl', 'php-gd', 'php-soap', 'php-xml', 'php-zip','php-ldap', 
        '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo instalar php.")
        rollback()
    else:
        print("\t[*] Php instalado.")
    print("\t[-] Configurando php.")
    t = threading.Thread(target=spin)
    t.start()
    cmd = "sed -i -e 's/;extension=ldap/extension=ldap/' \
           -i -e 's/;extension=openssl/extension=openssl/' \
           -i -e 's/;extension=pgsql/extension=pgsql/' -i -e 's/upload_max_filesize = 2M/upload_max_filesize = 2G/'\
           -i -e 's/post_max_size = 8M/post_max_size = 8G/' /etc/php/7.3/apache2/php.ini"
    info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo configurar php.")
        rollback()
    else:
        print("\t[*] Php configurado.")

    print("\t[-] Instalando git.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','install','git','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se puede instalar git.")
        rollback()
    else:
        print("\t[*]Git instalado.")

    print("\t[-] Instalando/verificando drush.")
    info = subprocess.Popen(['wget','https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar', '-q','--show-progress']).wait()
    if info != 0:
        print("\t[!] No se pudo descargar drush")
        rollback()
    else:
        print("\t[*] Drush descargado.")
    info = subprocess.Popen(['chmod','+x','drush.phar'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] No se pudo cambiar permisos a drush.")
        rollback()
    else:
        print("\t[*] Permisos asignados correctamente a drush")
    info = subprocess.Popen(['mv','drush.phar','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] No se pudo agregar drush al path")
        rollback()
    else:
        print("\t[*] Drush agregado al path")

    print("\t[-] Instalando cliente de postgresql")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','install','postgresql-client-11','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se puede instalar cliente de postgresql")
        rollback()
    else:
        print("\t[*] Cliente de postgresql instalado")

    print("\t[-] Instalando OpenSSL")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['apt-get','install','openssl','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se pudo instalar OpenSSL")
        rollback()
    else:
        print("\t[*] OpenSSL instalado")
    print("\t[--]Instalaciones para el funcionamiento de Drupal terminadas.")

def installDrupal(nombreSitio):
    print("\t[-] Descargando Drupal con drush.")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['drush', 'dl', 'drupal-8.8.4', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    t.do_run = False
    t.join()
    if info != 0:
        print("\t[!] No se ha descargado drupal 8.8.3.")
        rollback()
    else:
        print("\t[*] Drupal descargado")

    s1 = ""
    f = open(nombreSitio, "r")
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
                print(cad)
                break
    f.close()

    print("\t[-] Moviendo Drupal al sitio")
    info = subprocess.Popen(['mv', 'drupal-8.8.4/',cad]).wait()
    if info != 0:
        print("\t[!] No se pudo mover drupal")
        rollback()
    else:
        print("\t[*] Drupal ha sido movido")

    print("\t[-] Relizando instalacion de drupal")
    t = threading.Thread(target=spin)
    t.start()
    if flag :
    	url = "--db-url=pgsql://"+ usuarioDeBaseDatos1N +":"+contrasenaDeBaseDatos1N+"@"+ipServidorBaseDatos1N+":"+Puerto1N+"/"+NombreDeBaseDatosSitio1N
    else:
    	url = "--db-url=pgsql://"+ usuarioDeBaseDatos2N +":"+contrasenaDeBaseDatos2N+"@"+ipServidorBaseDatos2N+":"+Puerto2N+"/"+NombreDeBaseDatosSitio2N
    info = subprocess.Popen(['drush', 'si','standard',url, '-r', cad, '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    l = info.stdout.read().decode()
    l1 = l.find("Installation complete.")
    t.do_run = False
    t.join()
    if l1 == -1:
        print("\t[!] Problemas con la instalaciion")
        rollback()
    else:
        print("\t[*] Drupal instalado")
        print("[**] " + l[l1:l1+70])
    s1 = nombreSitio.split('/')
    print("\t[-] Activando modulos apache y sitio.")
    info = subprocess.Popen(['sudo','a2ensite', s1[-1]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] No se pudo activar la pagina")
        rollback()
    info = subprocess.Popen(['sudo','a2enmod', 'rewrite'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Error de activacion del modulo rewrite")
        rollback()
    info = subprocess.Popen(['sudo','a2enmod', 'ssl'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Error de activacion del modulo ssl")
        rollback()
    info = subprocess.Popen(['sudo','a2enmod', 'headers'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Error de activacion del modulo headers")
        rollback()
    print("\t[-] Reiniciando pagina.")
    info = subprocess.Popen(['/etc/init.d/apache2', 'restart']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Error Reiniciando apache")
        rollback()
    f = open(nombreSitio, "r")
    s1 = ""
    for linea in f:
        if linea.lower().find("servername") != -1:
            pat = re.compile(".*#.*servername.*")
            result = pat.match(linea.lower())
            if(result == None):
                l1 = linea.split()
                for j in l1[1:]:
                    s1+=j+' '
                s = s1.split('#')
                cad2 = s[0].rstrip().lstrip()
                break
    print("\t[-] Actualizando /etc/hosts.")
    cmd = "echo '127.0.0.1 "+cad2+"' >> /etc/hosts"
    info = subprocess.Popen(cmd,shell=True).wait()
    if info != 0:
        print("\t[!] Error al actualizar hosts")
        rollback()
    f.close()
    #migracion(cad)

def rollback():
    print("Realizando Rollback")
    info = subprocess.Popen(['apt', 'purge', 'php7.3', 'libapache2-mod-php7.3', 'php7.3-cli', 'php7.3-pgsql', 'php7.3-intl', 
        'php7.3-mysql', 'php7.3-curl', 'php7.3-gd', 'php7.3-soap', 'php7.3-xml', 'php7.3-zip','php7.3-ldap', '-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo desinstalar php")
    else:
        print("Php desinstalado")

    info = subprocess.Popen(['apt','purge','git','-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede desinstalar git")
    else:
        print("Git desinstalado")

    info = subprocess.Popen(['rm','/usr/bin/drush'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se pudo eliminar drush del path")
    else:
        print("Drush eliminado")
    info = subprocess.Popen(['apt','purge','postgresql-client-11','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede desinstalar cliente de postgresql")
    else:
        print("Cliente de postgresql desinstalado")

    info = subprocess.Popen(['apt','purge','openssl','-y'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("No se puede desinstalar OpenSSL")
    else:
        print("OpenSSL desinstalado")
    info = subprocess.Popen(['rm', '-r', 'drupal-8.8.3'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print(" drupal 8.8.3 No se pudo eliminar")
    else:
        print("Drupal eliminado")
    print("\t[*] Desinstalando ssh ya que no salio bien.")
    t = threading.Thread(target=spin)
    t.start()
    t.do_run = True
    cmd = "apt-get purge openssh-server -y"
    info = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()	
    t.do_run = False
    t.join()
    print("\t[*] Rollback realizado.")
    print("\t[*] Fin de ejecuciion.")
    sys.exit()

def migracion(cad):
    print("\t[-] Instalar/Habilitar modulos de migracion")
    t = threading.Thread(target=spin)
    t.start()
    info = subprocess.Popen(['drush', 'en', 'migrate_upgrade','-r',cad,'-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Problemas al habilitar el modulo migrate_upgrade")
        rollback()
    info = subprocess.Popen(['drush', 'en', 'migrate_plus','-r',cad, '-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Problemas al habilitar el modulo migrate_plus")
        rollback()
    info = subprocess.Popen(['drush', 'en', 'migrate_tools','-r',cad, '-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("\t[!] Problemas al habilitar el modulo migrate_tools")
        rollback()
    t.do_run = False
    t.join()
    print("\t[*] Modulos de migracion instalados y habilitados.")
    print("\t[-] Realizando migracion")
    #t = threading.Thread(target=spin)
    #t.start()
    if flag:
        url1 = "--legacy-db-url=pgsql://"+usuarioDeBaseDatos1+":"+contrasenaDeBaseDatos1+"@"+ipServidorBaseDatos1+"/"+NombreDeBaseDatosSitio2
        url= "--legacy-root=http://"+ipServidorBaseDatos1
    else:
        url1 = "--legacy-db-url=pgsql://"+usuarioDeBaseDatos2+":"+contrasenaDeBaseDatos2+"@"+ipServidorBaseDatos2+"/"+NombreDeBaseDatosSitio2
        url= "--legacy-root=http://"+ipServidorBaseDatos2
    info = subprocess.Popen(['drush', 'migrate_upgrade',url1,url,'--configure-only','-r',cad, '-y']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    #t.do_run = False
    #t.join()
    if info != 0:
        print("\t[!] Problemas al obtener datos de la migracion")
        rollback()
    else:
        print("\t[*] Se obtuvieron los datos a migrar")
    print("\t[-] Estado de migracion")
    info = subprocess.Popen(['drush', 'ms','-r',cad]).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Problemas estado de migracion")
        rollback()
    else:
        print("\t[*] Estado de la migracion")
    print("\t[-] Migrando datos")
    info = subprocess.Popen(['drush', 'mi', '--all','-r',cad]).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Error al migrar archivos")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Migracion completada")
    print("Estado de migracion")
    info = subprocess.Popen(['drush', 'ms','-r',cad]).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("Problemas estado de migracion")
        print("Abortando operacion")
        sys.exit()
    else:
        print("Estado de la migracion")

    print("Configuracion de sitio")
    info = subprocess.Popen(['drush','-y', 'config-set', 'system.perfermance','css.preprocess','0']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("css.preprocess")
        print("Abortando operacion")
        sys.exit()
    else:
        print("ccs.preprocess")
    print("Configuracion de sitio")
    info = subprocess.Popen(['drush','-y', 'config-set', 'system.perfermance','js.preprocess','0']).wait()#,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).wait()
    if info != 0:
        print("js.preprocess")
        print("Abortando operacion")
        sys.exit()
    else:
        print("js.preprocess")

print("Prerrequisito\n")
print("1)Haber ejecutado el  Script de base de datos\n")
opcion=input("s/[n] \tAdvertencia:en caso de continuar sin esto podra fallar la migracion\n")

if opcion == "s" or opcion == "S":
    installPre()
    nombreSitio1, nombreSitio2 = importSiteConf()
    installDrupal(nombreSitio1)
    flag = False
    installDrupal(nombreSitio2)
