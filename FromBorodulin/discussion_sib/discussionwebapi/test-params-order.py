# -*- coding: utf-8 -*-
from DiscussionService import *
import datetime
import urllib2

IP = "172.20.0.112"
PORT = "80"
PARAMS_NUMBER = 4 
TESTS_NUMBER = 1

if __name__ == "__main__":
    ds = DiscussionService(IP, PORT)
    
    timeslots = []
    presentations = []
    speakers = []
    for i in xrange(0, PARAMS_NUMBER):
        timeslots.append( ("Русский_текст_тимеслот" + str(datetime.datetime.now())) )
        presentations.append( ("Русский_текст_презентация" + str(datetime.datetime.now())) )
        speakers.append( ("Русский_текст_выступающий" + str(datetime.datetime.now())) )
   
    errors = 0
    for i in xrange(0, TESTS_NUMBER):
        r = ds.createThreads("test section", "today_" + str(datetime.datetime.now()),
         "test_section_" + str(datetime.datetime.now()), timeslots, presentations, speakers)
        if str(r) != "Success":
            errors += 1
	print urllib2.unquote(r)

    print "Errors/Tests: {}/{}".format(errors, TESTS_NUMBER)
