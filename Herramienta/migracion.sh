#!/bin/bash
read -p "Ingresa usuario de base de datos [drupaluser]: " name
name=${name:-drupaluser}
echo $name

read -p "Ingresa la contrasena [Hola123.,]: " pas
pas=${pas:-Hola123.,}
echo $pas

read -p "Ingresa ip [10.0.0.2]: " ip
ip=${ip:-10.0.0.2}
echo $ip

read -p "Ingresa base de datos [drupal711]: " db
db=${db:-drupal711}
echo $db

read -p "Ingresa ruta de drupal [/var/www/drupal7.11]: " ruta
ruta=${ruta:-/var/www/drupal7.11}
echo $ruta



cd $ruta
chown www-data:www-data -R $ruta
find $ruta -type f -exec chmod -v 644 {} +
find $ruta -type d -exec chmod -v 755 {} +

drush -y config-set system.performance css.preprocess 0
drush -y config-set system.performance js.preprocess 0

drush en migrate_upgrade -y
drush en migrate_plus -y
drush en migrate_tools -y
drush migrate-upgrade --legacy-db-url=pgsql://$name:$pas@$ip/db --legacy-root=http://$ip --configure-only

drush ms
drush mi --all
drush ms
drush -y config-set system.performance css.preprocess 0
drush -y config-set system.performance js.preprocess 0
