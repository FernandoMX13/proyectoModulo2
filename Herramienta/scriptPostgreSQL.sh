#!/bin/bash
archivoPostgresql="/etc/postgresql/11/main/postgresql.conf"
echo "Modificando Postgresql.conf ..."
if [ -r $archivoPostgresql ]; then
	sed -i -e 's/\#*listen_addresses = '\''localhost'\''/listen_addresses = '\''*'\''/' $archivoPostgresql
else
	echo "El archivo no es válido o no existe"
fi

read -p "Ingresa el nombre del propietario de la base de datos [drupaluser]: " name
name=${name:-drupaluser}
echo $name

read -p "Ingresa el nombre del propietario de la base de datos [drupaldb]: " database
database=${database:-drupaldb}
echo $database

read -p "Ingresa la contraseña [hola123.,]: " password
password=${password:-hola123.,}

echo "Modificando pg_hba.conf ..."
su -c "echo -e \"\nhost\t${name}\t${database}\t\t\tmd5\n\" >> /etc/postgresql/11/main/pg_hba.conf" postgres

echo "Creando usuario y base de datos.."
su -c "psql -c \"CREATE USER $name WITH ENCRYPTED PASSWORD '$password';\"" postgres
su -c "psql -c \"CREATE DATABASE $database WITH OWNER $name ENCODING 'UTF8' LC_COLLATE = 'es_MX.UTF-8' LC_CTYPE = 'es_MX.UTF-8';\"" postgres
su -c "psql -c \"ALTER DATABASE $database SET bytea_output = 'escape';\"" postgres


systemctl restart postgresql
echo "Listo :)"
