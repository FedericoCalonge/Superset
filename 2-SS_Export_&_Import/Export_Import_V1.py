#Ejemplo llamado: >python3 Export_Import_V1.py xxxxxxxxxxxxxxx
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

def delete_chart(id_chart,access_token):
	url_delete 	= 'http://localhost:8088/api/v1/chart/' + str(id_chart)
	response1 	= Session().delete(url_delete, 
						headers = {"authorization": "Bearer " + str(access_token)})
	print(response1.json)

def delete_dashboard(id_dashboard,access_token):
	url_delete 	= 'http://localhost:8088/api/v1/dashboard/' + str(id_dashboard)
	response1 	= Session().delete(url_delete, 
						headers = {"authorization": "Bearer " + str(access_token)})
	print(response1.json)

def export_dashboard(id_dashboard, access_token):
	url_get 	= 'http://localhost:8088/api/v1/dashboard/export/?q=[' + str(id_dashboard) + ']'
	response1 	= Session().get(url_get, 
						headers = {"authorization": "Bearer " + str(access_token)})
	json_codificado = (response1.content).decode('utf-8')
	print(json_codificado, file=open("output.json", "w"))

def import_dashboard(access_token):
	url_post 	= 'http://localhost:8088/api/v1/dashboard/import/'

	files = { 
	    'formData': (
	        "output.json", 
	        open("output.json", 'rb'), 
	        'application/json'
	    )
	}

	response = 	Session().post(		url_post, 
									files=files, 
									headers= {"authorization": "Bearer " + str(access_token)}
								)
	print(response)

#Main:
#id_chart 			= sys.argv[1] 		#ID del chart. Integer. Se pasa por CLI.
id_dashboard 		= sys.argv[1] 		#ID del dashboard. Integer. Se pasa por CLI.
access_token 		= login()
#delete_chart(id_chart,access_token)		#ANDA.
#delete_dashboard(id_dashboard,access_token) #ANDA.
export_dashboard(id_dashboard,access_token)	#ANDA, genera un json "output.json" que es el mismo que desde el navegador.
import_dashboard(access_token)	#ANDA, importa el json "output.json" que exportamos previamente.