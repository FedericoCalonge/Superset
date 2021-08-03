from requests import Session
import os
import json
from datetime import date, datetime

def Login():
    response   = Session().post('http://localhost:8088/api/v1/security/login', json={
                   "username": "admin",
                   "password": "admin",
                   "provider": "db",
                   "refresh": "true"
               })
    tokens     = response.json()
    return tokens.get("access_token")

def DeleteChart(id_chart,access_token):
    url_delete  = 'http://localhost:8088/api/v1/chart/' + str(id_chart)
    response   = Session().delete(url_delete, 
                        headers = {"authorization": "Bearer " + str(access_token)})

def DeleteDashboard(id_dashb,access_token):
    url_delete  = 'http://localhost:8088/api/v1/dashboard/' + str(id_dashb)
    response   = Session().delete(url_delete, 
                        headers = {"authorization": "Bearer " + str(access_token)})

def ExportDashboard(id_dashb, access_token):
    url_get     = 'http://localhost:8088/api/v1/dashboard/export/?q=[' + str(id_dashb) + ']'
    response   = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    #Genera un json "output.json" que es el mismo que genera al exportar desde el navegador.
    return (response.content.decode('utf-8'))

def ImportDashboard(access_token,archivo_json):
    url_get     = 'http://localhost:8088/api/v1/dashboard/import/'
    files       = { 
    'formData': (
        archivo_json, 
        open('Path_Jsons/' +archivo_json, 'rb'), 
        'application/json'
    )
}
    response   = Session().post(url_get, files=files,
                        headers = {"authorization": "Bearer " + str(access_token)})

def GetDashboardName(archivo_json):
    dashboard = ReadJSON(archivo_json)
    return(dashboard['dashboards'][0]['__Dashboard__']['dashboard_title']) #nombre del dashboard

def GetChartsID(id_dashb,access_token):
    lista           = []
    json_dashboard  = ExportDashboard(id_dashb, access_token)
    json_dashboard  = json.loads(json_dashboard)
    lista_charts    = json_dashboard['dashboards'][0]['__Dashboard__']['slices']
    for i in lista_charts:
        lista.append(i['__Slice__']['id'])

    return lista

def DeleteDashboardAndCharts(access_token, id_dashb):
    lista_ids_charts = GetChartsID(id_dashb,access_token)
    for id_chart in lista_ids_charts:
        DeleteChart(id_chart, access_token)
        print("Chart eliminado.")
    DeleteDashboard(id_dashb,access_token)
    print("Dashboard eliminado.")

def ReadJSON(json_dashboard):
    with open('Path_Jsons/' + json_dashboard) as json_file:
        data = json.load(json_file)
    return data

def GetListDashboards(access_token):
    url_get     = 'http://localhost:8088/api/v1/dashboard/'
    response    = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    response    = response.json()
    return(response)

def DashboardExist(nombre_dashboard,access_token):
    flag        = -1
    response    = GetListDashboards(access_token)
    for dash in response['result']:
        if(dash['dashboard_title'] == nombre_dashboard):
            flag = dash['id']
    return flag

def GenerateJSONsList():
    path_to_json    = 'Path_Jsons/'
    json_files      = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    return json_files

def BackupDashboard(id_dashb, access_token, nombre_dashboard):
    hoy    = str(datetime.today().replace(microsecond=0))
    url_get         = 'http://localhost:8088/api/v1/dashboard/export/?q=[' + str(id_dashb) + ']'
    response        = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    json_dashboard  = response.content.decode('utf-8')
    jsonFile        = open('Backups/'+nombre_dashboard+'_'+hoy+'.json', "w")
    jsonFile.write(json_dashboard)
    jsonFile.close()
    print("Backup realizado.")

def GetDashboard(id_dashboard, access_token):
    url_get         = 'http://localhost:8088/api/v1/dashboard/' + str(id_dashboard)
    response        = Session().get(url_get, 
                        headers = {"authorization": "Bearer " + str(access_token)})
    json_dashboard  = response.json()
    return(json_dashboard)

def AssembleJSON(dashboard_json):
    #Inicializamos new_json:
    new_json = {"css": "string","dashboard_title": "string","json_metadata": "string", "position_json": "string","published": "string","slug": "string"}
    #Carga de datos al new_json:
    new_json["dashboard_title"] = dashboard_json["result"]["dashboard_title"]
    new_json["css"]             = dashboard_json["result"]["css"]
    new_json["json_metadata"]   = dashboard_json["result"]["json_metadata"]
    new_json["position_json"]   = dashboard_json["result"]["position_json"]
    new_json["published"]       = dashboard_json["result"]["published"]
    new_json["slug"]            = dashboard_json["result"]["slug"]
    return(new_json)

def ModifyStateDashboard(id_dashboard, access_token):
    json_dashboard  = GetDashboard(id_dashboard, access_token)
    json_dashboard['result']['published'] = True
    json_modificado = AssembleJSON(json_dashboard)
    return(json_modificado)

def DraftToPublished(id_dashboard, access_token):
    json_modificado = ModifyStateDashboard(id_dashboard,access_token)
    url_put         = 'http://localhost:8088/api/v1/dashboard/' + str(id_dashboard)
    response        = Session().put(url_put, json = json_modificado, headers = {"authorization": "Bearer " + str(access_token)})

##################################################################################################################################################

print('Inicio Script Importación'+' - '+str(datetime.today().replace(microsecond=0)))
access_token = Login()
#Creamos una lista con todos los archivos .json que existen en la carpeta 'Path_Jsons/' ubicada donde se ejecuta el script:
lista = GenerateJSONsList()

if (len(lista)==0):
    raise ValueError('No hay dashboards a importar.')

for archivo_json in lista:
    nombre_dashboard    = GetDashboardName(archivo_json)
    #Recorremos la lista de dashboards en SS y veo uno por uno el que se llame igual y agarro su ID. En caso de no encontrar el ID devuelve -1:
    id_dashboard        = DashboardExist(nombre_dashboard, access_token) 
    if (id_dashboard == -1):
        ImportDashboard(access_token, archivo_json)
        print("Se crea Dashboard *"+nombre_dashboard+"* por primera vez junto a sus charts.")
        id_dashboard_nuevo    = DashboardExist(nombre_dashboard, access_token) 
        DraftToPublished(id_dashboard_nuevo, access_token)
    else:
        #Realizamos un backup en la carpeta 'Backups/' ubicada donde se ejecuta el script:
        BackupDashboard(id_dashboard, access_token, nombre_dashboard) 
        DeleteDashboardAndCharts(access_token, id_dashboard)
        ImportDashboard(access_token, archivo_json)
        print("Se crea Dashboard *"+nombre_dashboard+"* junto a sus charts.")
        id_dashboard_nuevo    = DashboardExist(nombre_dashboard, access_token) 
        DraftToPublished(id_dashboard_nuevo, access_token)

print('Finaliza Script Importación'+' - '+str(datetime.today().replace(microsecond=0)))
print(' ')
