sandbox/manage.py oscar_import_catalogue sandbox/fixtures/02_productos.csv
sandbox/manage.py loaddata sandbox/fixtures/03_productos_atributos.json
sandbox/manage.py loaddata sandbox/fixtures/01_Anzuelos/02_productos_anzuelos.json
sandbox/manage.py oscar_import_catalogue_images sandbox/fixtures/images.tar.gz
sandbox/manage.py update_index catalogue
