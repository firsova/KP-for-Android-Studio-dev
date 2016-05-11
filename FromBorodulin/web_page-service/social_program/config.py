import os
import cherrypy
curdir = os.path.dirname(__file__)

# Local IP Port
#SIB_IP = "192.168.112.109"
# SIB_IP = "172.20.64.10"
# SIB_PORT = 10010

# # World IP Port
# GLOBAL_SIB_IP = "194.85.173.9"
# GLOBAL_SIB_PORT = 10010

conf = {
	'/': {
		'tools.sessions.on': True,
		'tools.staticdir.root': curdir,
		'tools.template.on': True,
		'tools.encode.on': False,
		'tools.template.template': 'templates/social_program/social_program.html'
	},
	'/client': {
		'tools.template.on': True,
		'tools.template.template': 'templates/social_program/client/social_program.html',
		'tools.encode.on': False,
		'tools.sessions.on': True,
		'tools.staticdir.root': curdir
	},
	'/agenda': {
		'tools.template.on': True,
		'tools.template.template': 'templates/social_program/agenda-service/social_program.html',
		'tools.encode.on': False,
		'tools.sessions.on': True,
		'tools.staticdir.root': curdir
	},
	'/presentation': {
		'tools.template.on': True,
		'tools.template.template': 'templates/social_program/presentation-service/social_program.html',
		'tools.encode.on': False,
		'tools.sessions.on': True,
		'tools.staticdir.root': curdir
	},
	'/vote': {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [('Content-Type', 'text/plain')],
	},
	'/client_res': {
		'tools.staticdir.on': True,
		'tools.staticdir.root': curdir,
		'tools.staticdir.dir': '../templates/social_program/client'
	},
	'/agenda_res': {
		'tools.staticdir.on': True,
		'tools.staticdir.root': curdir,
		'tools.staticdir.dir': '../templates/social_program/agenda-service'
	},
	'/presentation_res': {
		'tools.staticdir.on': True,
		'tools.staticdir.root': curdir,
		'tools.staticdir.dir': '../templates/social_program/presentation-service'
	},
	'/socialprogramrequest': {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		'tools.encode.on' : True,
		'tools.encode.encoding' : 'utf-8'
	},
	'/restore': {
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [('Content-Type', 'text/plain')],
	}
}


def encode_str(str):
	# Encode string
	return str.encode('utf-8')
	
def decode_str(str):
	# Decode string
	return str.decode("string_escape").decode("utf-8")