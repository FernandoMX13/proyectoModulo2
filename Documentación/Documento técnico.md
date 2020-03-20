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

Estos archivos de configuración restringen el acceso a archivos de instalación y/o configuración del CMS, así como la redirección al index para los códigos de estado más comunes.

```
#
# Apache/PHP/Drupal settings:
#

# Protect files and directories from prying eyes.
<FilesMatch "\.(engine|inc|info|install|make|module|profile|test|po|sh|.*sql|theme|tpl(\.php)?|xtmpl)(~|\.sw[op]|\.bak|\.orig|\.save)?$|^(\.(?!well-known).*|Entries.*|Repository|Root|Tag|Template|composer\.(json|lock)|web\.config)$|^#.*#$|\.php(~|\.sw[op]|\.bak|\.orig\.save)$">
  <IfModule mod_authz_core.c>
    Require all denied
  </IfModule>
  <IfModule !mod_authz_core.c>
    Order allow,deny
  </IfModule>
</FilesMatch>

# Don't show directory listings for URLs which map to a directory.
Options -Indexes

# Follow symbolic links in this directory.
Options +FollowSymLinks

# Make Drupal handle any 404 errors.
ErrorDocument 404 /index.php

# Set the default handler.
DirectoryIndex index.php index.html index.htm

# Override PHP settings that cannot be changed at runtime. See
# sites/default/default.settings.php and drupal_environment_initialize() in
# includes/bootstrap.inc for settings that can be changed at runtime.

# PHP 5, Apache 1 and 2.
<IfModule mod_php5.c>
  php_flag magic_quotes_gpc                 off
  php_flag magic_quotes_sybase              off
  php_flag register_globals                 off
  php_flag session.auto_start               off
  php_value mbstring.http_input             pass
  php_value mbstring.http_output            pass
  php_flag mbstring.encoding_translation    off
</IfModule>

# Requires mod_expires to be enabled.
<IfModule mod_expires.c>
  # Enable expirations.
  ExpiresActive On

  # Cache all files for 2 weeks after access (A).
  ExpiresDefault A1209600

  <FilesMatch \.php$>
    # Do not allow PHP scripts to be cached unless they explicitly send cache
    # headers themselves. Otherwise all scripts would have to overwrite the
    # headers set by mod_expires if they want another caching behavior. This may
    # fail if an error occurs early in the bootstrap process, and it may cause
    # problems if a non-Drupal PHP file is installed in a subdirectory.
    ExpiresActive Off
  </FilesMatch>
</IfModule>

# Various rewrite rules.
<IfModule mod_rewrite.c>
  RewriteEngine on

  # Set "protossl" to "s" if we were accessed via https://.  This is used later
  # if you enable "www." stripping or enforcement, in order to ensure that
  # you don't bounce between http and https.
  RewriteRule ^ - [E=protossl]
  RewriteCond %{HTTPS} on
  RewriteRule ^ - [E=protossl:s]

  # Make sure Authorization HTTP header is available to PHP
  # even when running as CGI or FastCGI.
  RewriteRule ^ - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

  # Block access to "hidden" directories whose names begin with a period. This
  # includes directories used by version control systems such as Subversion or
  # Git to store control files. Files whose names begin with a period, as well
  # as the control files used by CVS, are protected by the FilesMatch directive
  # above.
  #
  # NOTE: This only works when mod_rewrite is loaded. Without mod_rewrite, it is
  # not possible to block access to entire directories from .htaccess, because
  # <DirectoryMatch> is not allowed here.
  #
  # If you do not have mod_rewrite installed, you should remove these
  # directories from your webroot or otherwise protect them from being
  # downloaded.
  RewriteRule "/\.|^\.(?!well-known/)" - [F]

  # If your site can be accessed both with and without the 'www.' prefix, you
  # can use one of the following settings to redirect users to your preferred
  # URL, either WITH or WITHOUT the 'www.' prefix. Choose ONLY one option:
  #
  # To redirect all users to access the site WITH the 'www.' prefix,
  # (http://example.com/... will be redirected to http://www.example.com/...)
  # uncomment the following:
  # RewriteCond %{HTTP_HOST} .
  # RewriteCond %{HTTP_HOST} !^www\. [NC]
  # RewriteRule ^ http%{ENV:protossl}://www.%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  #
  # To redirect all users to access the site WITHOUT the 'www.' prefix,
  # (http://www.example.com/... will be redirected to http://example.com/...)
  # uncomment the following:
  # RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
  # RewriteRule ^ http%{ENV:protossl}://%1%{REQUEST_URI} [L,R=301]

  # Modify the RewriteBase if you are using Drupal in a subdirectory or in a
  # VirtualDocumentRoot and the rewrite rules are not working properly.
  # For example if your site is at http://example.com/drupal uncomment and
  # modify the following line:
  # RewriteBase /drupal
  #
  # If your site is running in a VirtualDocumentRoot at http://example.com/,
  # uncomment the following line:
  # RewriteBase /

  # Pass all requests not referring directly to files in the filesystem to
  # index.php. Clean URLs are handled in drupal_environment_initialize().
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_URI} !=/favicon.ico
  RewriteRule ^ index.php [L]

  # Rules to correctly serve gzip compressed CSS and JS files.
  # Requires both mod_rewrite and mod_headers to be enabled.
  <IfModule mod_headers.c>
    # Serve gzip compressed CSS files if they exist and the client accepts gzip.
    RewriteCond %{HTTP:Accept-encoding} gzip
    RewriteCond %{REQUEST_FILENAME}\.gz -s
    RewriteRule ^(.*)\.css $1\.css\.gz [QSA]

    # Serve gzip compressed JS files if they exist and the client accepts gzip.
    RewriteCond %{HTTP:Accept-encoding} gzip
    RewriteCond %{REQUEST_FILENAME}\.gz -s
    RewriteRule ^(.*)\.js $1\.js\.gz [QSA]

    # Serve correct content types, and prevent mod_deflate double gzip.
    RewriteRule \.css\.gz$ - [T=text/css,E=no-gzip:1]
    RewriteRule \.js\.gz$ - [T=text/javascript,E=no-gzip:1]

    <FilesMatch "(\.js\.gz|\.css\.gz)$">
      # Serve correct encoding type.
      Header set Content-Encoding gzip
      # Force proxies to cache gzipped & non-gzipped css/js files separately.
      Header append Vary Accept-Encoding
    </FilesMatch>
  </IfModule>
</IfModule>

# Add headers to all responses.
<IfModule mod_headers.c>
  # Disable content sniffing, since it's an attack vector.
  Header always set X-Content-Type-Options nosniff
</IfModule>
ErrorDocument 301 http://alegrosito2.cert.unam.mx
ErrorDocument 302 http://alegrosito2.cert.unam.mx
ErrorDocument 400 http://alegrosito2.cert.unam.mx
ErrorDocument 401 http://alegrosito2.cert.unam.mx
ErrorDocument 403 http://alegrosito2.cert.unam.mx
ErrorDocument 404 http://alegrosito2.cert.unam.mx
ErrorDocument 500 http://alegrosito2.cert.unam.mx
ErrorDocument 503 http://alegrosito2.cert.unam.mx
ErrorDocument 504 http://alegrosito2.cert.unam.mx

<FilesMatch "(.*install.*|.*update.*|.*sql.*|.*config$|\.(engine|inc|info|install|make|module|profile|test|po|sh|.*sql|theme|tpl(\.php)?|xtmpl)$|^(\..*|Entries.*|Repository|Root|Tag|Template)$)">
  Require all denied
</FilesMatch>

```

### Instalación de utilerías, módulos y complementos

Los paquetes necesarios son realizados por el script, utilizando los siguientes comandos dentro de éste:

```bash
# apt-get update -y
# apt-get upgrade -y
# apt-get install apache2 -y
# apt-get install php7.3 libapache2-mod-php7.3 php7.3-cli php7.3-pgsql php7.3-intl php7.3-mysql php7.3-curl php7.3-gd php7.3-soap php7.3-xml php7.3-zip php7.3-ldap -y
# apt-get install git -y
# wget https://github.com/drush-ops/drush/releases/download/8.3.2/drush.phar -q --show-progress
# chmod +x drush.phar
# mv drush.phar /usr/bin/drush
# apt-get install postgresql-client-11 -y
# apt-get install openssl -y
# drush dl drupal-8.* -y
# apt-get install composer -y
```

### Ubicación de los archivos de la aplicación

La ruta de los archivos de configuración están establecidos en la línea de `DocumentRoot`, la cual establece la ubicación de los sitios y sus archivos.

## Funcionamiento de la aplicación

Esta aplicación consta de varios scripts, los cuales deben de ser ejecutados en los correspondientes equipos.

Para el equipo que almacena la base de datos, se debe de ejecutar el script `nombre`, el cual realiza la configuración de los bases de datos, usuarios y accesos a éstas.

Al ejecutarse el script de `importador.py` en la máquina que almacenará los sitios en sus versiones de Debian 10, ésta realiza una instalación de los paquetes necesarios para poder realizar la migración, así como la recepción de archivos. A su vez, en el equipo Debian 8 que contiene los sitios, se ejecuta el script `exportador.py` el cual manda al Debian 10 todos los archivos.

### Configuración de Apache

Los archvivos correspondientes a los sitios de drupal son llamados "drupal7-x.conf", donde "x" corresponde al número de sitio.

Cada uno de los archivos de configuración tienen el siguiente formato:

```
<IfModule mod_ssl.c>
        <VirtualHost _default_:443>
                ServerAdmin jose.colula@bec.seguridad.unam.mx

                ServerName alegrosito1.cert.unam.mx
                ServerAlias www.alegrosito1.cert.unam.mx

                DocumentRoot /var/www/drupal7.1

                <Directory "/var/www/drupal7.1/">
                        Options -Indexes +FollowSymLinks 
                        AllowOverride All
                        Require all granted
                </Directory>

                #LogLevel info ssl:warn
        RedirectMatch (install.php|update.php|\.txt$|.*xmlrpc.*) /
                ErrorLog ${APACHE_LOG_DIR}/drupal71ssl-error.log
                CustomLog ${APACHE_LOG_DIR}/drupal71ssl-access.log combined
        

        <IfModule mod_headers.c>
            Header set X-Content-Type-Options: "nosniff"
            Header set X-Frame-Options: "sameorigin"
            Header set X-XSS-Protection "1; mode=block"
        </IfModule>
                SSLEngine on
                SSLCertificateFile      /etc/ssl/certs/alegrosito1.crt
                SSLCertificateKeyFile /etc/ssl/private/alegrosito1.key

                <FilesMatch "\.(cgi|shtml|phtml|php)$">
                                SSLOptions +StdEnvVars
                </FilesMatch>
                <Directory /usr/lib/cgi-bin>
                                SSLOptions +StdEnvVars
                </Directory>

                BrowserMatch "MSIE [2-6]" \
                                nokeepalive ssl-unclean-shutdown \
                                downgrade-1.0 force-response-1.0
                # MSIE 7 and newer should be able to use keepalive
                BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown

        </VirtualHost>
</IfModule>
<VirtualHost *:80>
        ServerName alegrosito1.cert.unam.mx
        ServerAlias www.alegrosito1.cert.unam.mx

        ServerAdmin jose.colula@bec.seguridad.unam.mx
        DocumentRoot /var/www/drupal7.1

        #Redireccion a https
        RewriteEngine On
        RewriteCond %{HTTPS} !on
        RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
        
        <Directory "/var/www/drupal7.1">
                Options -Indexes +FollowSymLinks 
                AllowOverride All
                Require all granted
        </Directory>



        ErrorLog ${APACHE_LOG_DIR}/drupal71-error.log
        CustomLog ${APACHE_LOG_DIR}/drupal71-access.log combined

</VirtualHost>
```

Donde para cada sitio, le corresponde su respectivo _DocumentRoot_ y certificado SSL.

Adicional a esto, el el archivo _security.conf_ se le modifican las siguientes líneas para una mayor seguridad de los sitios:
```
ServerTokens ProductOnly
ServerSignature Off
TraceEnable Off
```

Los módulos que se requieren habilitar son los siguientes:
- poner aqui modulos

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

