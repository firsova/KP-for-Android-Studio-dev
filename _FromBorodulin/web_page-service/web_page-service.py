import os, os.path, sys
import random
import string
import json
import socket

curdir = os.path.dirname(__file__)
sys.path.append(curdir)

from config import *
import __builtin__
__builtin__.HOST = HOST
__builtin__.GLOBAL_SIB_IP = SIB_IP
__builtin__.GLOBAL_SIB_PORT = SIB_PORT

if __name__ == '__main__':  
    lan_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lan_ip.connect(("gmail.com",80))
    url = lan_ip.getsockname()[0]
    lan_ip.close()
    HOST = url + ":8080"
print HOST

BASE_URL = "http://127.0.0.1" + MOUNT_POINT
if HOST:
    BASE_URL = "http://" + HOST + MOUNT_POINT

__builtin__.BASE_URL = BASE_URL

import cherrypy
# Register the Mako plugin
from makoplugin import MakoTemplatePlugin
MakoTemplatePlugin(cherrypy.engine, base_dir=curdir).subscribe()

# Register the Mako tool
from makotool import MakoTool
cherrypy.tools.template = MakoTool()

import social_program
import chat

class WebPageService(object):
    @cherrypy.expose
    def index(self):
        return {'MOUNT_POINT' : MOUNT_POINT}
    
    @cherrypy.expose
    def restoreServiceUrls(self):
        if BASE_URL != None:
            social_program.restoreUrls()
            chat.restoreUrls()
        return 'OK - all urls restored'
    
    @cherrypy.expose
    def restoreSocialProgramUrls(self):
        if BASE_URL != None:
            social_program.restoreUrls()
        return 'OK - social program urls restored'
        
    @cherrypy.expose
    def restoreChatUrls(self):
        if BASE_URL != None:
            chat.restoreUrls()
        return 'OK - chat service url restored'

web_page_app = WebPageService()
    
if __name__ == '__main__':  
    lan_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lan_ip.connect(("gmail.com",80))
    url = lan_ip.getsockname()[0]
    lan_ip.close()
    # mc.set("web-page-url", "http://" + str(url) + ":8080" + MOUNT_POINT + "/sp")
    # web_page_kp.publish_MOUNT_POINTs("http://" + str(url) + ":8080" + MOUNT_POINT + "/sp")
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })
                            
    cherrypy.tree.mount(web_page_app, MOUNT_POINT, conf)
    cherrypy.tree.mount(social_program.social_program_app, MOUNT_POINT+social_program.MOUNT_POINT, social_program.conf)
    cherrypy.tree.mount(chat.chat_app, MOUNT_POINT+chat.MOUNT_POINT, chat.conf)
    print web_page_app.restoreServiceUrls()
    
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # web_page_kp.publish_MOUNT_POINTs(BASE_URL + "/sp")
    # mc.set(BASE_URL + "/sp")
    
    cherrypy.tree.mount(web_page_app, MOUNT_POINT, conf)
    cherrypy.tree.mount(social_program.social_program_app, MOUNT_POINT+social_program.MOUNT_POINT, social_program.conf)     
    cherrypy.tree.mount(chat.chat_app, MOUNT_POINT+chat.MOUNT_POINT, chat.conf)
    print web_page_app.restoreServiceUrls()
    
    # Disable the autoreload which won't play well
    cherrypy.config.update({'engine.autoreload.on': False})

    # let's not start the CherryPy HTTP server
    cherrypy.server.unsubscribe()

    # use CherryPy's signal handling
    cherrypy.engine.signals.subscribe()

    # Prevent CherryPy logs to be propagated
    # to the Tornado logger
    cherrypy.log.error_log.propagate = False

    # Run the engine but don't block on it
    cherrypy.engine.start()

    application = cherrypy.tree