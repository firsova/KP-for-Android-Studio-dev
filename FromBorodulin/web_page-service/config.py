import os
import cherrypy
curdir = os.path.dirname(__file__) 

# Local IP Port
#SIB_IP = "192.168.112.109"
SIB_IP = "172.20.64.10"
SIB_PORT = 10010

# World IP Port
#SIB_IP = "194.85.173.9"
#SIB_PORT = 10010

MOUNT_POINT = "/page"
HOST = "smartroom.cs.karelia.ru"

conf = {
	'/': { 
		'tools.sessions.on': True,
		'tools.staticdir.root': curdir,
		'tools.template.on': True,
		'tools.encode.on': False,
		'tools.template.template': 'templates/index.html'
	}
}

def encode_str(str):
	# Encode string
	return str.encode('utf-8')
	
def decode_str(str):
	# Decode string
	return str.decode("string_escape").decode("utf-8")