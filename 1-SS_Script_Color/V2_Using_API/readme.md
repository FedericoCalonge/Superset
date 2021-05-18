Descripcion: nos logueamos en SS mediante la libreria superset-api-client y modificamos los colores de los labels en los dashboards deseados (mediante GET y POSTs). El dashboard se guardará automáticamente en SS.

Librerias a instalar:
* apt-get install python3-tk
* pip3 install superset-api-client
* pip3 install dataclasses (si se tiene python3.6 o inferior)

Parametros utilizados (2):
* a) ID del dashboard - Integer - Ejemplo: 20
* b) Label a modificar - String - Ejemplo: "Ingresadas"

Ejemplo de utilizacion: 
* python3 Mod_Color.py 20 "Ingresadas" --> Asi se cambia el color del label "Ingresadas" en el dashboard con id "20".
