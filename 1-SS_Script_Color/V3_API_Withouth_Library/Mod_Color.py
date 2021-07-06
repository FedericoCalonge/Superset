#Ejemplo llamado: >python3 Mod_Color.py 20 "Ingresadas"
from requests import Session
import sys
import json

def login():
	#Con Session() python genera una cookie de session (es distinta a la que vemos en el navegador al darle a "Inspect").
	response = Session().post('http://localhost:8088/api/v1/security/login', 
				json = {
	            "username": "admin",
	            "password": "admin",
	            "provider": "db",
	            "refresh": "true"
	        	})
	tokens 	= response.json()
	#print (response, tokens)  #Devuelve 200 y 2 tokens (access_token y refresh_token).
	return tokens.get("access_token")

def get_dashboard(id, access_token):
	url_get 	= 'http://localhost:8088/api/v1/dashboard/' + str(id)
	response 	= Session().get(url_get, 
						headers = {"authorization": "Bearer " + str(access_token)})
	response 	= response.json()
	return(response)

def ElegirColor():
    import tkinter as tk
    from tkinter.colorchooser import askcolor
    win = None
    if not tk._default_root:
        win = tk.Tk()
        win.wm_withdraw()
    color = askcolor()
    if win is not None: 
        win.destroy()
    return color[1]

def ExisteLabel(my_json,label):
	json_metadata1 = my_json["result"]["json_metadata"]
	json_metadata2 = json.loads(json_metadata1)
	return label in json_metadata2["label_colors"]

def assemble_json(dashboard_json):
	#Inicializamos new_json:
	new_json = {"css": "string","dashboard_title": "string","json_metadata": "string","position_json": "string","published": True,"slug": "string"}
	#Carga de datos al new_json:
	new_json["dashboard_title"] = dashboard_json['result']['dashboard_title']
	new_json["css"] 			= dashboard_json["result"]["css"]
	new_json['json_metadata'] 	= dashboard_json['result']['json_metadata']
	new_json["position_json"] 	= dashboard_json["result"]["position_json"]
	new_json["published"] 		= dashboard_json["result"]["published"]
	new_json["slug"] 			= dashboard_json["result"]["slug"]
	return(new_json)

def put_dashboard(id, access_token,json_modificado):
	url_put 	= 'http://localhost:8088/api/v1/dashboard/' + str(id)
	response1 	= Session().put(url_put, json = json_modificado, headers = {"authorization": "Bearer " + str(access_token)})
	#print(response1)

def CambiarColor(dashboard_json,access_token, id_dashboard, label_a_modificar):
	color_hexa = ElegirColor()
	if (color_hexa is None):
		raise ValueError('Se cancelo la modificacion de color')
	#Modificamos el color al label_a_modificar dentro del dashboard_json:
	json_metadata1 = dashboard_json["result"]["json_metadata"]
	json_metadata1 = json.loads(json_metadata1)
	json_metadata1["label_colors"][label_a_modificar] = color_hexa
	json_string = json.dumps(json_metadata1)
	dashboard_json["result"]["json_metadata"] = json_string
	new_json = assemble_json(dashboard_json)
	put_dashboard(id_dashboard,access_token,new_json)

#Main:
id_dashboard 		= sys.argv[1] 		#ID del dashboard. Integer. Se pasa por CLI.
label_a_modificar 	= sys.argv[2]	#Label del dashboard a modificar. String. Se pasa por CLI.
access_token 		= login()
dashboard_json 		= get_dashboard(id_dashboard, access_token)
if not (ExisteLabel(dashboard_json,label_a_modificar)):
	raise ValueError('No existe el label a modificar')
CambiarColor(dashboard_json,access_token, id_dashboard, label_a_modificar)

""""
1-Te devuelve el access_token:
curl -X POST "http://localhost:8088/api/v1/security/login" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"password\":\"admin\",\"provider\":\"db\",\"refresh\":true,\"username\":\"admin\"}"
2-Usas el token: ...despues de Bearer hay que poner el access_token que devuelve arriba:
curl -X GET "http://localhost:8088/api/v1/query/" -H  "accept: application/json" -H  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjEzNTAwMDQsIm5iZiI6MTYyMTM1MDAwNCwianRpIjoiMzE3MzVmMzUtNTU4Yi00NjNkLWI3YmItOWY2YjdlZThmZjAxIiwiZXhwIjoxNjIxMzUwOTA0LCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.oGXrjkjwp-OxF596BKZWP4v9dVON42H-hc9dsfQRWSk"
"""
