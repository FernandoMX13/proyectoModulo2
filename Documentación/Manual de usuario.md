# Manual de usuario

## Descripción de la herramienta

Esta herramienta es un conjunto de distintos scripts que se utilizan para la importación y exportación de dos sitios web, los cuales va a ser actualizados a versiones más recientes de las que actualmente se encuentran. En este caso, los sitios se encuentran en un sistema operativo Debian 8 y con un CMS Drupal 7.69 y se actualizará a un sistema operativo Debian 10 con un CMS Drupal 8.

## Cómo utilizar la herramienta

Esta herramienta se debe de ejecutar en dos equipos de cómputo:

### Debian 8

#### Requisitos: 
- Tener instalado la útlima versión de pyhton.
- Una versión de cliente de PostgreSQL versión 11.
- Conexión a internet.

En una shell, con permisos de root, ejecutar el programa de la siguiente manera:
```bash
# python3 exportador.py
```

### Debian 10
#### Requisitos: 
- Tener instalado la útlima versión de pyhton.
- Conexión a internet.

En una shell, con permisos de root, ejecutar el programa de la siguiente manera:
```bash
# python3 importador.py
```

### Debian 10 (Bases de Datos)
#### Requisitos
- Tener instalado PostgreSQL y un cliente de éste.
- Tener instalado php y php-pgsql.
- Tener el usuario _postgres_ habilitado.

En una shell, ejecutar el programa de la siguiente manera:
```bash
# ./scriptPostgreSQL.sh
```