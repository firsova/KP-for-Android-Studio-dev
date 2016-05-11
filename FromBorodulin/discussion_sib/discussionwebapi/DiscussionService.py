
"""
	Simple implimentation Discussion-Service WEB API
	2015 (c) Sergei Podkopaev
"""
__author__ = 'Sergei Podkopaev'
__version__ = '0.1.0'


import urllib2
import urllib
import sys
from urls import *

class DiscussionService:
    d_ip = None
    d_port = None
    urlStartPoint = None
    
    def __init__(self, d_ip, d_port):
        """
            :param: d_ip - Disqussion-Service IP (string)
            :param: d_port - Disqussion-Service port (80 ?) (integer)
        """
        self.d_ip = d_ip
        self.d_port = d_port
        self.urlStartPoint = "http://" + d_ip + ":" + str(d_port)
    
    def setCurrentConference(self, conference_uuid):
        url_part = ""
        params = []

        if conference_uuid is None:
            url_part = ENDCURRENTSECTION
        else:
            url_part = SETCURRENTSECTION 
            params.append(("section_uuid", str(conference_uuid)))
        params.append((ACCESSPOINT, ACCESSCODE))
        url = self.urlStartPoint + url_part + urllib.urlencode(params)
        print url
        f = urllib2.urlopen(url)
        sys.stderr.write("setCurrentConference: {}\n".format(f.read()))


    def setCurrentPresentation(self, timeslot_uuid):
        url_part = ""
        params = []
        if timeslot_uuid is None:
            url_part = ENDCURRENTPRESENTATION
        else:
            url_part = SETCURRENTPRESENTATION
            params.append(("timeslot_uuid", timeslot_uuid))
        params.append((ACCESSPOINT, ACCESSCODE))
        url = self.urlStartPoint + url_part + urllib.urlencode(params)
        print url
        f = urllib2.urlopen(url)
        sys.stderr.write("setCurrentPresentation: {}\n".format(f.read()))
        

    def createThreads(self, sectionTitle, sectionDate, sectionUUID, timeslotUUIDs, 
                        presentationTitles, speakers):
        params = []
        params.append(("sectionTitle", sectionTitle))
        params.append(("sectionDate", sectionDate))
        params.append(("sectionUUID", sectionUUID))
        
        if len(timeslotUUIDs) == len(speakers) \
            and len(speakers) == len(presentationTitles):
            for i in xrange(0, len(timeslotUUIDs)):
                params.append(("timeslotUUIDs[]", timeslotUUIDs[i]))
    
            for i in xrange(0, len(presentationTitles)):
                params.append(("presentationTitles[]", presentationTitles[i]))
    
            for i in xrange(0, len(speakers)):
                params.append(("speakers[]", speakers[i]))
                
            params.append((ACCESSPOINT, ACCESSCODE))
            p = urllib.urlencode(params)
            url = self.urlStartPoint + CREATETHREADS
            print "Create URL: " + url + p
            f = urllib2.urlopen(url, p)
            result = f.read()
            return result
        else:
            print "\tLengths of timeslotUUIDs, presentationTitles, speakers arrays: {} {} {}\nNot going to create threads\n".format(len(timeslotUUIDs), \
                len(presentationTitles), len(speakers))
            print str(timeslotUUIDs) + "\n" + str(presentationTitles) + "\n" + speakers + "\n\n\n"
            return None



    def getPosts(self, seconds):
        sec_str = str(seconds)
        url_part = GETPOSTS
        url = self.urlStartPoint + url_part
        url += "%s"
        url = url%(urllib.urlencode({"seconds" : sec_str}))
        url += "&" + ACCESSPOINT + "=" + ACCESSCODE
        print url
        f = urllib2.urlopen(url)
        result = f.read()
        
        return result

   
