# Documento técnico

## Descripción de la aplicación

La aplicación está diseñada para lograr una migración de sitios previamente configurado en un Drupal 7.69 hacia una configuración en Drupal 8. 

Es una herramienta desarrollada en lenguaje python, la cual realiza comandos de shell para la descarga e instalación de paquetes necesarios para la correcta configuración e instalación del CMS de Drupal 8.

## Como instalar la aplicación

No requiere de instalación.

### Prerequisitos de la aplicación

Para que esta aplicación pueda funcionar correctamente, es necesario que contar con:

- Python 3.4 o superior instalado en la máquina que almacenará los sitios en Drupal 8.

- Postgres instalado en la máquina que almacenará la base datos de los sitios en Drupal 9, junto con el usuario postgres ya configurado para la creación de usuarios y bases de datos.

- Haber realizado un `apt-get update` y `apt-get upgrade -y` en la máquina Debian 8, la cual es la que almacena los sitios originialmente en la versión 7.69 de Drupal.

- Si los sitios cuentan con autenticación ldap y un servidor smtp, éste debe de ser capaz de comunicarse con la máquina Debian 10.

### Paquetes a instalar

- drush
- git
- apache2
- php7.3, libapache2-mod-php7.3, php7.3-cli, php7.3-pgsql, php7.3-intl, php7.3-mysql, php7.3-curl, php7.3-gd, php7.3-soap, php7.3-xml, php7.3-zip, php7.3-ldap
- openssl

### Archivos y configuración

Por poner

### Instalación de utilerías, módulos y complementos

Realizadas por el script

### Ubicación de los archivos de la aplicación

Pendiente

## Funcionamiento de la aplicación REVISAR!!!!

Esta aplicación consta de varios scripts, los cuales deben de ser ejecutados en los correspondientes equipos.

Para el equipo que almacena la base de datos, se debe de ejecutar el script `nombre`, el cual realiza...

Al ejecutarse la aplicación en la máquina que almacenará los sitios en sus versiones de Debian 10, ésta realiza una instalación de los paquetes necesarios para poder realizar la migración...

### Configuración de Apache

Apache se configura de tal modo que...

### Configuración de PostgreSQL

PostgreSQL cuenta con una configuración de seguridad tal que...