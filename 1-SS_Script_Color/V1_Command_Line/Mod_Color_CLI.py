import json
from datetime import datetime
import sys

def LeerJson(Archivo):
	with open(Archivo) as json_file:
		data = json.load(json_file)
	return data
	
def CrearJson(my_json):
	filename=datetime.now()
	with open(str(filename), 'w') as json_file:
		json.dump(my_json, json_file)

def ExisteLabel(my_json,label):
	return label in my_json['label_colors']

#Main:
color_hexa="#"+sys.argv[3]  		#Color en hexa. String
label_a_modificar=sys.argv[2]  	#Nombre del label a modificar. String
my_json=LeerJson(sys.argv[1])    	#Archivo json
if not (ExisteLabel(my_json,label_a_modificar)):
	raise ValueError('No existe el label a modificar')
my_json['label_colors'][label_a_modificar]=color_hexa
CrearJson(my_json)
