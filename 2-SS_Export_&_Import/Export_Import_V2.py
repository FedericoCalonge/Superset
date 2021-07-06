#Ejemplo llamado: >python3 Mod_Color.py 20 "Ingresadas"
from requests import Session
import sys
import json

def login_ambiente_1():
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


def login_ambiente_2():
	#Con Session() python genera una cookie de session (es distinta a la que vemos en el navegador al darle a "Inspect").
	response = Session().post('http://localhost:8088/api/v1/security/login',  #CAMBIAR URL.
				json = {
	            "username": "admin",
	            "password": "admin",
	            "provider": "db",
	            "refresh": "true"
	        	})
	tokens 	= response.json()
	#print (response, tokens)  #Devuelve 200 y 2 tokens (access_token y refresh_token).
	return tokens.get("access_token")

#Main:
id_dashboard 		= sys.argv[1] 		#ID del dashboard. Integer. Se pasa por CLI.
login_ambiente_1
login_ambiente_2