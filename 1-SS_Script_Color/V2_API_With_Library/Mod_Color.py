#Parametros utilizados (2): 
##### a)ID del dashboard  - Integer - Ejemplo: 70
##### b)Label a modificar - String  - Ejemplo: "Dinero recaudado"
#Ejemplo de utilizacion:
#python3 3-ModColor_GUI.py 8 "Classic Cars"

import json
from datetime import datetime
import sys

def ExisteLabel(my_json,label):
    return label in my_json['label_colors']

def ElegirColor():
    import tkinter as tk
    from tkinter.colorchooser import askcolor
    win = None
    if not tk._default_root:
        win = tk.Tk()
        win.wm_withdraw()
    color = askcolor(color=None)
    if win is not None: 
        win.destroy()
    return color[1]

def ObtenerJsonAndDashboard(id_d):
    from supersetapiclient.client import SupersetClient
    client = SupersetClient(
        host="http://localhost:8088/",
        username="admin",
        password="admin",
        )
    dashboard =  client.dashboards.find(id=id_d)[0]
    return dashboard.json_metadata, dashboard

def CambiarColor(my_dashboard, label_a_modificar, color_hexa):
    my_dashboard.update_colors({
        label_a_modificar: color_hexa
    })
    my_dashboard.save()

id_dashboard=sys.argv[1] #ID del dashboard. Integer. Se pasa por CLI.
my_json, my_dashboard=ObtenerJsonAndDashboard(id_dashboard)
color_hexa=ElegirColor()
if (color_hexa is None):
	raise ValueError('Se cancelo la modificacion de color')	
label_a_modificar=sys.argv[2]  #Nombre del label a modificar. String. Se pasa por CLI.
if not (ExisteLabel(my_json,label_a_modificar)):
    raise ValueError('No existe el label a modificar')
CambiarColor(my_dashboard, label_a_modificar, color_hexa)
