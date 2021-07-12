from requests import Session
import os
import json

def Login():
	response = Session().post('http://localhost:8088/api/v1/security/login', json={
	            "username": "admin",
	            "password": "admin",
	            "provider": "db",
	            "refresh": "true"
	        })
	tokens = response.json()
	return tokens.get("access_token")

def DeleteChart(id_chart,access_token):
    url_delete     = 'http://localhost:8088/api/v1/chart/' + str(id_chart)
    response1     = Session().delete(url_delete, 
                        headers = {"authorization": "Bearer " + str(access_token)})

def DeleteDashboard(id_dashb,access_token):
    url_delete     = 'http://localhost:8088/api/v1/dashboard/' + str(id_dashb)
    response1     = Session().delete(url_delete, 
                        headers = {"authorization": "Bearer " + str(access_token)})

def ExportDashboard(id_dashb, access_token):
    url_get     = 'http://localhost:8088/api/v1/dashboard/export/?q=[' + str(id_dashb) + ']'
    response1     = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    return (response1.content.decode('utf-8'))
    #Genera un json "output.json" que es el mismo que genera al exportar desde el navegador.

def ImportDashboard(access_token,archivo_json):
    url_get     = 'http://localhost:8088/api/v1/dashboard/import/'
    files = { 
    'formData': (
        archivo_json, 
        open('Path_Jsons/' +archivo_json, 'rb'), 
        'application/json'
    )
}
    response1     = Session().post(url_get, files=files,
                        headers = {"authorization": "Bearer " + str(access_token)})
    #print(response1.json)

def ObtenerNombreDashboard(archivo_json):
    dashboard=LeerJson(archivo_json)
    return(dashboard['dashboards'][0]['__Dashboard__']['dashboard_title']) #nombre del dashboard

def ObtenerIdCharts(id_dashb,access_token):
    lista=[]
    json_dashboard=ExportDashboard(id_dashb, access_token)
    json_dashboard=json.loads(json_dashboard)
    lista_charts=json_dashboard['dashboards'][0]['__Dashboard__']['slices']
    for i in lista_charts:
        lista.append(i['__Slice__']['id'])

    return lista

def DeleteDashboardAndCharts(access_token,archivo_json,id_dashb):
    lista_ids_charts=ObtenerIdCharts(id_dashb,access_token)
    for id_chart in lista_ids_charts:
        DeleteChart(id_chart, access_token)
    DeleteDashboard(id_dashb,access_token)
    
def LeerJson(json_dashboard):
    with open('Path_Jsons/' + json_dashboard) as json_file:
        data = json.load(json_file)
    return data

def ObtenerListaDashboards(access_token):
    url_get     = 'http://localhost:8088/api/v1/dashboard/'
    response     = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    response     = response.json()
    return(response)

def ExisteDashboard(nombre_dashboard,access_token):
    flag=-1
    response=ObtenerListaDashboards(access_token)
    for i in response['result']:
        if(i['dashboard_title']==nombre_dashboard):
            flag=i['id']
    return flag

def GenerarListaJsons():
    path_to_json = 'Path_Jsons/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    return json_files

access_token = Login()
lista=GenerarListaJsons()  #Se crea una lista con todos los archivos .json que hay en la carpeta Path_Jsons/ ubicada donde se ejecuta el script.
#print(lista)

for archivo_json in lista:
    nombre_dashboard=ObtenerNombreDashboard(archivo_json)
    id_dashboard=ExisteDashboard(nombre_dashboard, access_token) #Recorro la lista de dashboards en SS y veo uno por uno el que se llame igual y agarro su ID. En caso de no encontrar el ID devuelve -1.
    if id_dashboard==-1:
        ImportDashboard(access_token, archivo_json)
    else:
        ImportDashboard(access_token, archivo_json)
        DeleteDashboardAndCharts(access_token, archivo_json, id_dashboard)