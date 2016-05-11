# -*- coding: utf-8 -*-

'''
	Discussion service
'''

import cherrypy
import urllib
import sys
import os, os.path
import socket
import locale
import datetime
import time
import calendar
import urllib

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from disqusapi import DisqusAPI
from disqusapi import APIError
from disqusdb.DisqusDB import DisqusDB
from Disqus import Disqus
from exception_handler import *
from templates.template_creator import *
from config import *
from kp import *
import kp

DEBUG_MSG = "DEBUG ({}):".format(os.path.basename(__file__))

MOUNT_POINT = "/chat"
LOCAL_BASE_URL = BASE_URL + MOUNT_POINT

if LOCALE == "RU":
	ERR_MSG_NO_PRESENTATIONS_AT_THE_MOMENT = "В настоящий момент не проходит ни одна презентация"
	ERR_MSG_NO_CONFERENCE_AT_THE_MOMENT = "В настоящий момент не проходит ни одна конференция"
	ERR_MSG_THREAD_NOT_FOUND = "Ветка дискуссии не найдена"
	ERR_MSG_THREADS_NOT_FOUND = "Ветки дискуссии не найдены"
	ERR_MSG_DISCUSSIONS_NOT_FOUND = "Обсуждения не найдены"
	ERR_MSG_FORBIDDEN = "403 Forbidden"
else:
	ERR_MSG_NO_PRESENTATIONS_AT_THE_MOMENT = "No presentations at the moment"
	ERR_MSG_NO_CONFERENCE_AT_THE_MOMENT = "No conference at the moment"
	ERR_MSG_THREAD_NOT_FOUND = "Thread was not found"
	ERR_MSG_THREADS_NOT_FOUND = "Threads were not found"
	ERR_MSG_DISCUSSIONS_NOT_FOUND = "Discussions were not found"
	ERR_MSG_FORBIDDEN = "403 Forbidden"

'''
	Creates web pages for discussion service ans handles users' requests
'''
class ChatService(object):
	def __init__(self):
		
		self.disqus_db = DisqusDB()
		self.base_url = LOCAL_BASE_URL

	'''
		Shows the Disqus chat widget of the current presentation (no params) or any chosen presentation (identifier, section_uuid are required)
	'''
	@cherrypy.expose
	def index(self, identifier = None):
		try:
			disqus = Disqus()
			section_uuid = None
			if not identifier:
				event = self.disqus_db.get_current_event()
				if not event:
					print DEBUG_MSG + "{}: No current event\n".format(sys._getframe().f_code.co_name)
					template = create_template("error")
					return template.render(base_url = self.base_url, message = ERR_MSG_NO_PRESENTATIONS_AT_THE_MOMENT)
				section_uuid, identifier = event
				if not identifier:
					print DEBUG_MSG + "{}: Identifier in event is None\n".format(sys._getframe().f_code.co_name)
					template = create_template("error")
					return template.render(base_url = self.base_url, message = ERR_MSG_NO_PRESENTATIONS_AT_THE_MOMENT)
			thread = None
			thread = self.disqus_db.get_thread_from_db(identifier)
			if thread is None:
				print DEBUG_MSG + "{}: No such thread with identifier={}\n".format(sys._getframe().f_code.co_name, identifier)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_THREAD_NOT_FOUND)
			thread_id, category_id, presentation_title, speaker, section_title = thread

			category = self.disqus_db.get_categories_from_db(category_id)
			if category:
				category = category.pop()
				category_id, section_uuid, section_title = category


			print DEBUG_MSG + "{}: base_url={}, identifier={}, section_title={}, presentation_title={}, speaker={}\n".format(sys._getframe().f_code.co_name, \
				self.base_url, identifier, section_title, presentation_title, speaker)
			template = create_template("index")
			return template.render(base_url = self.base_url, 
									identifier = identifier, 
									forum = disqus.forum, 
									section_title = section_title, 
									presentation_title = presentation_title,
									speaker = speaker)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Shows list of all sections with links to lists of corresponding threads
	'''
	@cherrypy.expose
	def listCategories(self):
		try:
			categories = []
			categories = self.disqus_db.get_categories_from_db()
			if not categories:
				print DEBUG_MSG + "{}: Categories array is empty\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_DISCUSSIONS_NOT_FOUND)
			else:
				print DEBUG_MSG + "{}: base_url={}, categories={}\n".format(sys._getframe().f_code.co_name, self.base_url, categories)
				template = create_template("listCategories")
				return template.render(base_url = self.base_url, categories = categories)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Shows list of threads for the current section with links to corresponding Disqus chat widgets
	'''
	@cherrypy.expose
	def listCurrentThreads(self):
		try:
			current_event = self.disqus_db.get_current_event()
			if not current_event:
				print DEBUG_MSG + "{}: current_event is None\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_NO_CONFERENCE_AT_THE_MOMENT)
			section_uuid = ""
			section_uuid, identifier = current_event
			if not section_uuid:
				print DEBUG_MSG + "{}: section_uuid is None\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_NO_CONFERENCE_AT_THE_MOMENT)
			print DEBUG_MSG + "{}: section_uuid={}".format(sys._getframe().f_code.co_name, section_uuid)
			return self.listThreads(section_uuid)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()
	
	'''
		Shows list of threads for any chosen section with links to corresponding Disqus chat widgets
	'''
	@cherrypy.expose
	def listThreads(self, section_uuid):
		try:
			threads = []
			threads = self.disqus_db.get_threads_from_db(section_uuid)
			if not threads:
				print DEBUG_MSG + "{}: Threads array is empty\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_THREADS_NOT_FOUND)
			section_title = ""
			section_title = threads.pop()
			# This error should never occur but still...
			if not section_title:
				print DEBUG_MSG + "{}: Section_title is None\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_THREAD_NOT_FOUND)
			threads = threads.pop()
			if not threads:
				print DEBUG_MSG + "{}: Threads array is empty\n".format(sys._getframe().f_code.co_name)
				template = create_template("error")
				return template.render(base_url = self.base_url, message = ERR_MSG_THREADS_NOT_FOUND)
			else:
				print DEBUG_MSG + "{}: base_url={}, threads={}, section_title={}\n".format(sys._getframe().f_code.co_name, self.base_url, threads, section_title)
				template = create_template("listThreads")
				return template.render(base_url = self.base_url, threads = threads, section_title = section_title)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()


'''
	Interface to the SIB-module for creating threads on Disqus.com, 
	setting current sections/presentations for chat service 
	and for getting list of messages of the current presentation
'''
class WebAPI(object):
	def __init__(self):
		self.disqus_db = DisqusDB()
		self.access_code = ACCESS_CODE

	'''
		Sets a section with given section_uuid as current
	'''
	@cherrypy.expose
	def setCurrentSection(self, section_uuid, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		try:
			print DEBUG_MSG + "{}: Setting current section to {}...\n".format(sys._getframe().f_code.co_name, section_uuid)
			return self.disqus_db.set_current_section(section_uuid)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Sets a presentation with given timeslot_uuid as current. A section must be set as current before that.
	'''
	@cherrypy.expose
	def setCurrentPresentation(self, timeslot_uuid, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		try:
			print DEBUG_MSG + "{}: Setting current presentation to {}...\n".format(sys._getframe().f_code.co_name, timeslot_uuid)
			return self.disqus_db.set_current_presentation(timeslot_uuid)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Sets the current section and presentation as finished
	'''
	@cherrypy.expose
	def endCurrentSection(self, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		try:
			print DEBUG_MSG + "{}: Ending current section...\n".format(sys._getframe().f_code.co_name)
			return self.disqus_db.end_current_section()
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Sets the current presentation as finished
	'''
	@cherrypy.expose
	def endCurrentPresentation(self, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		try:
			event = self.disqus_db.get_current_event()
			if not event:
				print DEBUG_MSG + "{}: Ending current presentation failed: no current section\n".format(sys._getframe().f_code.co_name)
				return "No current section"
			print DEBUG_MSG + "{}: Ending current presentation...\n".format(sys._getframe().f_code.co_name)
			return self.disqus_db.end_current_presentation()
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Creates a new category and threads on Disqus.com for given section and presentations
	'''
	@cherrypy.expose
	#def createThreads(self, sectionTitle = None, sectionDate = None, sectionUUID = None, timeslotUUIDs = None, presentationTitles = None, speakers = None):
	def createThreads(self, *args, **kwargs):
	#def createThreads(self):
		try:
			disqus = Disqus()

			access_code = kwargs["access_code"]
			if access_code != self.access_code:
				return ERR_MSG_FORBIDDEN
			sectionTitle = kwargs["sectionTitle"]
			sectionDate = kwargs["sectionDate"]
			sectionUUID = kwargs["sectionUUID"]
			timeslotUUIDs = []
			for a in kwargs["timeslotUUIDs[]"]:
				timeslotUUIDs.append(a)
			presentationTitles = []
			for a in kwargs["presentationTitles[]"]:
				presentationTitles.append(a)
			speakers = []
			for a in kwargs["speakers[]"]:
				speakers.append(a)

			if not isinstance(sectionTitle, str):
				sectionTitle = sectionTitle.encode("utf-8")
			if not isinstance(sectionDate, str):
				sectionDate = sectionDate.encode("utf-8")
			if not isinstance(sectionUUID, str):
				sectionUUID = sectionUUID.encode("utf-8")
			for i in xrange(0, len(timeslotUUIDs)):
				if not isinstance(timeslotUUIDs[i], str):
					timeslotUUIDs[i] = timeslotUUIDs[i].encode("utf-8")
			for i in xrange(0, len(presentationTitles)):
				if not isinstance(presentationTitles[i], str):
					presentationTitles[i] = presentationTitles[i].encode("utf-8")
			for i in xrange(0, len(speakers)):
				if not isinstance(speakers[i], str):
					speakers[i] = speakers[i].encode("utf-8")


			'''
			sectionTitle = "The most epic conference'2015"
			sectionDate = "28.07.2015"
			sectionUUID = "secuuid_" + str(time.time())
			timeslotUUIDs = ["tslotuuid_" + str(time.time()), "tslotuuid_" + str(time.time()) + "_2", "tslotuuid_" + str(time.time()) + "_3"]
			presentationTitles = ["Проблема падающих на спину пингвинов и её решения", "Размышления о времени, которое мы потратили на производственную практику", "Сколько нужно бобров, чтобы вкрутить лампочку в розетку? Исследовательская работа"]
			speakers = ["Иванов И.И.", "Просто", "Джон Сноу"]
			'''
			print DEBUG_MSG + "{}: Creating threads on Disqus.com...\n".format(sys._getframe().f_code.co_name)
			return disqus.create_threads(sectionTitle, sectionDate, sectionUUID, timeslotUUIDs, presentationTitles, speakers)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Returns comments on the current presentation for the last given minutes
	'''
	@cherrypy.expose
	def getPosts(self, seconds, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		try:
			disqus = Disqus()
			try:
				sinceSeconds = int(seconds.encode("utf-8"))
			except ValueError:
				sinceSeconds = 0
			print DEBUG_MSG + "{}: Retrieving recent posts from Disqus.com...\n".format(sys._getframe().f_code.co_name)
			return disqus.get_posts(sinceSeconds)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

	'''
		Does synchronization with Disqus.com: just deletes all entries in 'category' and 
		'thread' tables in the DB and fills them again with data stores at Disqus.com
	'''
	@cherrypy.expose
	def synchDisqus(self, access_code):
		if access_code != self.access_code:
			return ERR_MSG_FORBIDDEN
		if not ALLOW_SYNCH:
			print DEBUG_MSG + "{}: Synch is disabled in configuration file\n".format(sys._getframe().f_code.co_name)
			return "Synch is disabled in configuration file\n"
		try:
			disqus = Disqus()
			print DEBUG_MSG + "{}: Starting synchronization with Disqus.com...\n".format(sys._getframe().f_code.co_name)
			return disqus.synch_disqus(force = True)
		except Exception as e:
			return error_handler(e)
		except:
			return error_handler()

conf = {
	'/': {
		'tools.sessions.on': True,
		'tools.staticdir.root': file_dir,
		'tools.encode.on': False,
	},
	'/static': {
		'tools.staticdir.on': True,
		'tools.staticdir.dir': './public',
	},
	'/webapi' : {
		'tools.sessions.on': False,
		'tools.encode.on': False,
	}
}

chat_app = ChatService()
chat_app.webapi= WebAPI()
discussion_kp = WebPageProcessor(GLOBAL_SIB_IP, GLOBAL_SIB_PORT)

def restoreUrls():
    discussion_kp.publish_service_urls(BASE_URL + MOUNT_POINT)

# if __name__ == '__main__':	
	# cherrypy.config.update({'server.socket_host': '0.0.0.0',
							# 'server.socket_port': 8080,
							# })
	# cherrypy.quickstart(chat_app, MOUNT_POINT, app_conf)
# else:
	# wsgiapp = cherrypy.Application(chat_app, MOUNT_POINT, config = app_conf)
	# application = wsgiapp
	# cherrypy.config.update({'engine.autoreload.on': False})
	# cherrypy.server.unsubscribe()
	# cherrypy.engine.start()

# try:
	# discussion_kp = WebPageProcessor(GLOBAL_SIB_IP, GLOBAL_SIB_PORT) 
	# publish_result = discussion_kp.publish_service_urls(LOCAL_BASE_URL)
	# print DEBUG_MSG + "Publishing service URL resulted in: {}\n".format(publish_result)
# except Exception as e:
	# print "Publishing service URL failed: " + error_handler(e)
# except:
	# print "Publishing service URL failed: " + error_handler()
