import os, os.path, sys
import random
import string
import json

MOUNT_POINT = "/sp"

curdir = os.path.dirname(__file__)
sys.path.append(curdir)

import cherrypy
import appglobals

# Include kp class and config
from kp import *
import kp
from config import *

# # Register the Mako plugin
# from makoplugin import MakoTemplatePlugin
# MakoTemplatePlugin(cherrypy.engine, base_dir=curdir).subscribe()

# # Register the Mako tool
# from makotool import MakoTool
# cherrypy.tools.template = MakoTool()

print GLOBAL_SIB_IP + ' / ' + str(GLOBAL_SIB_PORT)
print HOST + ' ' + BASE_URL

social_program_kp = WebPageProcessor(GLOBAL_SIB_IP, GLOBAL_SIB_PORT) 

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=True)

if mc.get("socialProgram") == None:
    mc.set("socialProgram", encode_str(appglobals.socialProgram))

def restoreUrls():
    if BASE_URL != None:
        social_program_kp.publish_service_urls(BASE_URL + MOUNT_POINT)
    
class SocialProgramService(object):
    @cherrypy.expose
    def index(self):
        return {}
        
    # @cherrypy.expose
    # def socialProgramRestoreUrls(self):
        # restoreUrls()
        # return 'OK'

class SocialProgramClient(object):
    @cherrypy.expose
    def index(self, person_uuid='c768abd-3'):
        #print mc.get("socialProgram")
        return {'social_program': decode_str(mc.get("socialProgram")),
                'person_uuid' : person_uuid}
                
class SocialProgramAgenda(object):
    @cherrypy.expose
    def index(self):
        return {'social_program': decode_str(mc.get("socialProgram"))}

class SocialProgramPresentation(object):
    @cherrypy.expose
    def index(self):
        return {'social_program': decode_str(mc.get("socialProgram"))}

class VoteWebService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return '1'

    def POST(self, placeslot_uuid=None, person_uuid=None, vote=None):
        #print vote + ' from ' + person_uuid
        social_program_kp.publish_vote_result(placeslot_uuid, person_uuid, vote)
        social_program_kp.notification_voteUpdate(placeslot_uuid)
        
class SocialProgramRequestService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **args):
        return decode_str(mc.get("socialProgram"))

    def POST(self, service_uuid=None, social_program=None):
        #global socialProgramJSON
        #print 'from ' + service_uuid + ' with json\n' + encode_str(social_program) 
        mc.set("socialProgram",encode_str(social_program))
        #print 'read from memory ' + decode_str(mc.get("socialProgram"))
        return 'OK'
        
class SocialProgramRestoreUrls(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **args):
        restoreUrls()
        return 'OK'
        
social_program_app = SocialProgramService()
social_program_app.client = SocialProgramClient()
social_program_app.agenda = SocialProgramAgenda()
social_program_app.presentation = SocialProgramPresentation()
social_program_app.vote = VoteWebService()
social_program_app.socialprogramrequest = SocialProgramRequestService()
social_program_app.restore = SocialProgramRestoreUrls()