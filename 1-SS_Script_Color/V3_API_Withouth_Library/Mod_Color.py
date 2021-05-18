from requests import Session
import sys

def login():
	#Con Session() python genera una cookie de session (es distinta a la que vemos en el navegador al darle a "Inspect")
	response = Session().post('http://localhost:8088/api/v1/security/login', json={
	            "username": "admin",
	            "password": "admin",
	            "provider": "db",
	            "refresh": "true"
	        })

	response.raise_for_status()
	tokens = response.json()
	#print (response, tokens)  #Devuelve 200 y 2 tokens (access_token y refresh_token)
	return tokens.get("access_token")

def get_dashboard(id, access_token):
	url_get = 'http://localhost:8088/api/v1/dashboard/' + str(id)
	access_token_armado = "Bearer " + str(access_token)
	response = Session().get(url_get, 
						headers ={"authorization": access_token_armado})
	response.raise_for_status()
	response = response.json()
	return(response)

def modificar(dashboard):
	dashboard['result']['dashboard_title']='Titulo_Modificado'
	return dashboard

def put_dashboard(id, access_token,json_modificado):
	url_put = 'http://localhost:8088/api/v1/dashboard/' + str(id)
	Session().put(url_put,data=json_modificado,headers ={"authorization": "Bearer " + str(access_token)})
	# probar con.... --> json={json_modificado}

#Main:
id_dashboard=sys.argv[1] #ID del dashboard. Integer. Se pasa por CLI.
access_token = login()
dashboard = get_dashboard(id_dashboard, access_token)
print (dashboard)
print(dashboard['result']['dashboard_title'])
dashboard_mod = modificar(dashboard)
print(dashboard_mod['result']['dashboard_title'])
put_dashboard(id_dashboard,access_token,dashboard_mod)

#Get al nuevo dashboard:
dashboard_n = get_dashboard(id_dashboard, access_token)
print("Ultimo: "+ dashboard_n['result']['dashboard_title'])

""""
	1-Te devuelve el access_token:
curl -X POST "http://localhost:8088/api/v1/security/login" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"password\":\"admin\",\"provider\":\"db\",\"refresh\":true,\"username\":\"admin\"}"

	2-Usas el token: ...despues de Bearer hay que poner el access_token que devuelve arriba:
curl -X GET "http://localhost:8088/api/v1/query/" -H  "accept: application/json" -H  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjEzNTAwMDQsIm5iZiI6MTYyMTM1MDAwNCwianRpIjoiMzE3MzVmMzUtNTU4Yi00NjNkLWI3YmItOWY2YjdlZThmZjAxIiwiZXhwIjoxNjIxMzUwOTA0LCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.oGXrjkjwp-OxF596BKZWP4v9dVON42H-hc9dsfQRWSk"
"""
