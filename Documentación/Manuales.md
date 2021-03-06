# Manuales

## Integrantes

- Ayala San Juan Luis Antonio
- Colula Morales José Alberto
- Hernández Vázquez Edgar
- Resendiz Cruz Luis Fernando
- Urbina Garrido Mauricio

## Definición del proyecto

Se trata de una herramienta divida en una serie de scripts dedicados a minimizar el contacto del usuario, y su objetivo principal es el de instalar Drupal 8.8.4 en un Debian 10, el cual tiene requisitos mínimos de funcionamiento.

Además, la herramienta consta de 3 servidores: 
- Base de datos en PostgreSQL configurado en un Debian 10
- LDAP y SMTP configurados en un Debian 10
- WAF configurado en un Debian 10
- Sitios instalados y migrados en un Debian 10

## Metas y objetivos alcanzados

### Metas

Las metas de este proyecto fueron...

- Instalación y configuración de dos sitios en drupal 7.69, en conjunto de su respectiva base de datos, un servidor SMTP y LDAP.
- Migración de los sitios drupal 7.69 almacenados en una equipo Debian 8 a Drupal 8 que se almacenarán en un equipo Debian 10.
- Instalación de un WAF en configuración de proxy inverso que provee de seguridad a los sitios actualizados.
- Tener control de acceso a usuarios y roles específicos con privilegios a los sitios instalados.

### Objetivos alcanzados

Los objetivos alcanzados fueron:
- Instalación de dos sitios en drupal 7.69 con contenido multimedia y temas variados.
- Conexión a una base de datos remota
- WAF pendiente
- Autenticación LDAP

## Referencias

- Matei Cezar, M. (2017, 12 octubre). Install a Complete Mail Server with Postfix and Webmail in Debian 9. Recuperado 20 marzo, 2020, de https://www.tecmint.com/install-postfix-mail-server-with-webmail-in-debian/
- Debian 10 Configuration Tutorial : Server World. (2019, 26 julio). Recuperado 20 marzo, 2020, de https://www.server-world.info/en/note?os=Debian_10
- Debian 10 Configuration Tutorial : Server World. (2019, 26 julio). Recuperado 20 marzo, 2020, de https://www.server-world.info/en/note?os=Debian_10
- Mauricio Dinarte, M. D. (s.f.). Writing your first Drupal migration. Recuperado 21 marzo, 2020, de https://agaric.coop/blog/writing-your-first-drupal-migration
- COPIAS DE SEGURIDAD DE SITIOS DRUPAL CON DRUSH. (s.f.). Recuperado 21 marzo, 2020, de https://www.solucionex.com/blog/copias-de-seguridad-de-sitios-drupal-con-drush
- Drupal. (s.f.-b). Access to this page has been denied.. Recuperado 21 marzo, 2020, de https://www.drupal.org/docs/8/upgrade/upgrade-using-drush
- Drupal. (s.f.-c). Access to this page has been denied.. Recuperado 21 marzo, 2020, de https://www.drupal.org/docs/8/upgrade

- Download & Extend modules. (s.f.). Recuperado 20 marzo, 2020, de https://www.drupal.org/project/project_module
- Access to this page has been denied.. (s.f.). Recuperado 20 marzo, 2020, de https://www.drupal.org/
- Access to this page has been denied.. (2018, 28 septiembre). Recuperado 20 marzo, 2020, de https://www.drupal.org/docs/7/backing-up-and-migrating-a-site/migrating-a-site
- Home - Drush docs. (s.f.). Recuperado 20 marzo, 2020, de https://docs.drush.org/en/master/