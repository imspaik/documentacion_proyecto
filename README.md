# Guia de instalacion del proyecto


### Requisitos previos ###
Para poder instalar este proyecto, se necesitan los paquetes "nodejs" y "npm".

CLI> sudo apt install nodejs

CLI> sudo apt install npm

### Creacióon de un entorno virtual ###
Para crear el entorno virtual necesitaremos "pip" 

CLI> sudo apt-get install python3-pip

En caso de tener pip instalado, instalamos el paquete "virtualenv"

CLI> sudo pip3 install virtualenv

Ahora creamos el entorno virtual con el comando:

CLI> virtualenv nombre_de_tu_entorno -p python3

Y por ultimo activamos el entorno:

CLI> source nombre_entorno_virtual/bin/activate

### Despliegue de Django Oscar ###
Primero instalamos django oscar

CLI> pip install django-oscar

Luego ejecutamos el siguiente comando

CLI> make sandbox

Este comando desplegará la tienda online (La Pescaleta), aplicacion web (Gadifishing), CMS Wegtail y un blog.
Ademas de todo lo anterior creará la base del catalogo de nuestra tienda (categorias, atributos, variantes...) ademas de los productos.

### Ejecución del proyecto ###
Para lanzar todo y que sea accesible desde el navegador escribimos el comando:

Si queremos que sea accesible desde cualquier host de la red

CLI> python3 sandbox/manage.py runserver 0.0.0.0:8000

Para que solo sea accesible desde nuestro host

CLI> python3 sandbox/manage.py runserver

Y ya podemos acceder desde: http://localhost:8000/
