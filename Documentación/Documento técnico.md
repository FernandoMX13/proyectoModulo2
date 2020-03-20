# Documento técnico

## Descripción de la aplicación

La aplicación está diseñada para lograr una migración de sitios previamente configurado en un Drupal 7.69 hacia una configuración en Drupal 8. 

Es una herramienta desarrollada en lenguaje python, la cual realiza comandos de shell para la descarga e instalación de paquetes necesarios para la correcta configuración e instalación del CMS de Drupal 8.

## Como instalar la aplicación

### Prerequisitos de la aplicación

Para que esta aplicación pueda funcionar correctamente, es necesario contar con:

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

#### PHP

Para el correcto funcionamiento de los sitios juntos en conjunto del módulo de LDAP, se deben de descomentar las siguientes líneas en el archivo _/etc/php/7.3/apache2/php.ini_
```
extension=ldap
extension=openssl
extension=pgsql
```

#### LDAP

Para la configuración de LDAP, se descargaron los paquetes `slapd` y `ldap-utils`, el cual nos pedirá un nombre de dominio, en nuestro caso, es _ldap-smtp.cert.unam.mx_. En automático, slapd agarra la configuración de dominio para poder crear usuarios y grupos.

Primeramente, se debe de crear un archivo llamado _base.ldif_, el cual contendrá la configuración para usuarios y grupos:

```
dn: ou=people,dc=unam,dc=mx
objectClass: organizationalUnit
ou: people

dn: ou=groups,dc=unam,dc=mx
objectClass: organizationalUnit
ou: groups
```

Posterior a esto, se crean archivos con los datos de los usuarios. Un ejemplo es el archivo _ldapbeto.ldif_ el cual contiene los datos del usuatio "beto":

```
dn: uid=beto,ou=people,dc=unam,dc=mx
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: beto
sn: colula
userPassword: {SSHA}JPaZXeZFGuTw6Z41OF7ZkYy8ptQuqPoA
loginShell: /bin/bash
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/beto

dn: cn=beto,ou=groups,dc=unam,dc=mx
objectClass: posixGroup
cn: beto
gidNumber: 1001
memberUid: beto
```

Para el campo de `userPassword`, ser requiere previamente ejecutar el comando `slappasswd`, el cual nos pedirá una contraseña para generar, y devolverá un valor `{SSHA}xxxxxxxxxxxxxxxxx`, el cual corresponde a la respectiva contraseña del usuario en su archivo.

Finalmente, para agregar al usuario al sistema de LDAP, se ejecuta el siguiente comando:

`ldapadd -x -D cn=admin,dc=srv,dc=world -W -f ldapbeto.ldif`

#### SMTP

Para el funcionamiento de SMTP, se requiere de la instalación de los paquetes `curl, net-tools, bash-completion, wget, lsof, mailutils, dovecot-core, dovecot-imapd`. Adicionalmente, se descarga _Rainloop Webmail_ para tener una interfaz gráfica de nuestro servidor de correo.

Los archivos de configuración respectivos a SMTP son los siguientes:

- main.cf
```
# /etc/postfix/main.cf
smtpd_banner = $myhostname ESMTP
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 2

# TLS parameters
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_use_tls=yes
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache

smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated dated defer_unauth_destination
myhostname = ldap-smtp.cert.unam.mx
mydomain = cert.unam.mx
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
myorigin = $mydomain
mydestination = $myhostname, cert.unam.mx, localhost.$mydomain , localhost
relayhost =
mynetworks = 127.0.0.0/8 10.0.0.5/24
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = ipv4

home_mailbox = Maildir/

# SMTP-Auth settings
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $myhostname
smtpd_recipient_restrictions = permit_mynetworks,permit_auth_destination,permit_sasl_authenticated,reject
```
- dovecot.conf
```
# /etc/dovecot/dovecot.conf
!include_try /usr/share/dovecot/protocols.d/*.protocol

listen = *, ::

dict {
  #quota = mysql:/etc/dovecot/dovecot-dict-sql.conf.ext
  #expire = sqlite:/etc/dovecot/dovecot-dict-sql.conf.ext
}

!include conf.d/*.conf

!include_try local.conf
```
- 10-auth.conf
```
# /etc/dovecot/conf.d/10-auth.conf
disable_plaintext_auth = no
auth_mechanisms = plain login
#!include auth-deny.conf.ext
#!include auth-master.conf.ext

!include auth-system.conf.ext
#!include auth-sql.conf.ext
#!include auth-ldap.conf.ext
#!include auth-passwdfile.conf.ext
#!include auth-checkpassword.conf.ext
#!include auth-vpopmail.conf.ext
#!include auth-static.conf.ext
```
- 10-mail.conf
```
# /etc/dovecot/conf.d/10-mail.conf
mail_location = maildir:~/Maildir
namespace inbox {
  inbox = yes
}

mail_privileged_group = mail

protocol !indexer-worker {

}
```
- 10-master.conf
```
# /etc/dovecot/conf.d/10-master.conf

service imap-login {
  inet_listener imap {
    #port = 143
  }
  inet_listener imaps {
    #port = 993
    #ssl = yes
  }
}

service pop3-login {
  inet_listener pop3 {
    #port = 110
  }
  inet_listener pop3s {
    #port = 995
    #ssl = yes
  }
}

service submission-login {
  inet_listener submission {
    #port = 587
  }
}

service lmtp {
  unix_listener lmtp {
    #mode = 0666
  }

  # Create inet listener only if you can't use the above UNIX socket
  #inet_listener lmtp {
    # Avoid making LMTP visible for the entire internet
    #address =
    #port = 
  #}
}

service imap {
  # limit if you have huge mailboxes.
  #vsz_limit = $default_vsz_limit

  # Max. number of IMAP processes (connections)
  #process_limit = 1024
}

service pop3 {
  # Max. number of POP3 processes (connections)
  #process_limit = 1024
}

service submission {
  # Max. number of SMTP Submission processes (connections)
  #process_limit = 1024
}

service auth {
  unix_listener auth-userdb {
    #mode = 0666
    #user = 
    #group = 
  }

  # Postfix smtp-auth
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
    user = postfix
    group = postfix
  }

  # Auth process is run as this user.
  #user = $default_internal_user
}

service auth-worker {
}

service dict {
  unix_listener dict {
    #mode = 0600
    #user = 
    #group = 
  }
}
```

Una vez realizado estas configuraciones, tendremos listo nuestro servidor SMTP.

#### WAF

EDGAAAAAR!!!!

#### Drupal .htaccess

Falta poner

### Instalación de utilerías, módulos y complementos

Los paquetes necesarios son realizados por el script, utilizando los siguientes comandos dentro de éste:

```bash
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
```

### Ubicación de los archivos de la aplicación

La ruta de los archivos de configuración están establecidos en la línea de `DocumentRoot`, la cual establece la ubicación de los sitios y sus archivos.

## Funcionamiento de la aplicación

Esta aplicación consta de varios scripts, los cuales deben de ser ejecutados en los correspondientes equipos.

Para el equipo que almacena la base de datos, se debe de ejecutar el script `nombre`, el cual realiza...

Al ejecutarse la aplicación en la máquina que almacenará los sitios en sus versiones de Debian 10, ésta realiza una instalación de los paquetes necesarios para poder realizar la migración...

### Configuración de Apache

Los archvivos correspondientes a los sitios de drupal son llamados "drupal7-x.conf", donde "x" corresponde al número de sitio.

.......

### Configuración de PostgreSQL

Para la correcta administración de la base de datos, se necesita del usuario _postgres_, el cual hará la creación de las bases de datos para los sitios, así como la creación y asignación de un usuario para administrar dichas bases de datos.

En el proyecto realizado, se creo el usuario _drupaluser_, el cual administra todas las bases de datos de todos los sitios (drupal71, drupal72, drupal81, drupal82).

Se configuró el archivo _pg_hba.conf_ de tal forma que se necesite autenticación para ingresar a las bases de datos.

```
# Database administrative login by Unix domain socket
local   all             postgres                                md5
local    drupal71    drupaluser                md5
local    drupal72    drupaluser                md5
local    drupal81    drupaluser                md5
local   drupal82        drupaluser                              md5

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             drupaluser      0.0.0.0/0            md5
#host    all             drupaluser      10.0.0.1/24              md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     all                                     peer
#host    replication     all             127.0.0.1/32            md5
#host    replication     all             ::1/128                 md5
```

