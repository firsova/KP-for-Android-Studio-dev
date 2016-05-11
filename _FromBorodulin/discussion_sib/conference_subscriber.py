# -*- coding: utf-8 -*-
"""
    Conference Subscriber
    2015 (c) Sergei Podkopaev
"""
__author__ = 'Sergei Podkopaev'
__version__ = '0.3.0'


from smart_m3.m3_kp import *
import uuid
from ontology import *
from config import *
import sys
from discussionwebapi import *
import signal
from multiprocessing import Process, Queue
import time
import json
import os, os.path
from exception_handler import *

DEBUG_MSG = "\nDEBUG ({}):".format(os.path.basename(__file__))
DEBUG_MODE = True

class SIBInternalError(Exception):
    """
        Class SIBInternalError(Exception)
    This exception means that something going wrong with 
    getting data from SIB orm aybe some required 
    data in SIB was not initialized.
    It supports only ASCII symbols
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class KPHandler:
    node = None

    def __init__(self, node):
        self.node = node
            
    def get_current_timeslot(self):
        triple = [Triple(None, URI(PROPERTY_CURRENTTIMESLOT), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            raise SIBInternalError("Cannot get title of section")
        return str(result[0][2])

    def get_section_info(self, section_uuid):
        """
        Getting section title and section date by section_uuid
        It throws the SIBInternalError exception if it cannot get this data
        """
        
        # Section Title
        triple = [Triple(URI(section_uuid), URI(PROPERTY_SECTIONTITLE), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            raise SIBInternalError("Cannot get title of section")
        result_str = self._rdf_result_cp1251_to_utf8(result[0][2])

        print "Section title: {}".format(result_str)
        self.section_title = result_str

        # Section Date
        triple = [Triple(URI(section_uuid), URI(PROPERTY_SECTIONDATE), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            raise SIBInternalError("Cannot get section date")

        print "Section date: {}".format(str(result[0][2]))
        self.section_date = str(result[0][2])

    def get_presentation_from_timeslots(self, section_uuid):
        """
        It looks over list of timeslots and gets some info about presentation
        for each of them.
        This method throws SIBInternalError if it cannot get uuid of first timeslot
        in the section.
        """

        triple = [Triple(URI(section_uuid), URI(PROPERTY_FIRSTTIMESLOT), None)]
        result = self.node._rdf_query(triple)

        if self.check_triples(result) is False:
            sys.stderr.write("Error: can't get FIRSTTIMESLOT\n")
            raise SIBInternalError("Error: can't get FIRSTTIMESLOT\n\n section_uuid = {}".format(section_uuid))
        current_timeslot = result[0][2]
        has_next = True

        while has_next:
            presentation_title = "No title"
            presentation_speaker = "No speaker"
            triple = None
            try:
                presentation_title = self.get_timeslot_title(current_timeslot)
                if presentation_title == "No title":
                    print "Can't get timeslot title. Getting presentation title..."
                    presentation_ID = self.get_presentation_id(current_timeslot)
                    if presentation_ID is not None:
                        print "Presentation ID: {}".format(presentation_ID)
                        presentation_title = self.get_presentation_title(presentation_ID)
                    else:
                        sys.stderr.write("ERROR: Can't get presentation title. Setting title = \"No Title\"\n")
                        presentation_title = "No title"
                print "Presentation title: {}".format(presentation_title)

                presentation_speaker = self.get_presentation_speaker(current_timeslot)
                print "Presentation speaker: {}\n".format(presentation_speaker)
            except Exception as e:
                sys.stderr.write(error_handler(e))
            except:
                sys.stderr.write(error_handler())

            self.timeslot_uuids.append(strip_hashtag(current_timeslot))
            self.presentation_speakers.append(presentation_speaker)
            self.presentation_titles.append(presentation_title)

            triple = [Triple(URI(current_timeslot), URI(PROPERTY_NEXTTIMESLOT), None)]
            result = self.node._rdf_query(triple)
            if self.check_triples(result) is False:
                has_next = False
            else:
                current_timeslot = result[0][2]

    def get_timeslot_title(self, timeslot_uuid):
        """
        :param timeslot_uuid: uuid of the timeslot

        :return: Timeslot title in UTF8
        """

        triple = [Triple(URI(timeslot_uuid), URI(PROPERTY_TIMESLOTTITLE), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is  False:
            return "No title"
        return self._rdf_result_cp1251_to_utf8(result[0][2])

    def get_presentation_id(self, timeslot):
        """
        :param timeslot: uuid of the timeslot

        :return: URL with presentation uuid or None if there's no presentation uuid

        It raises SIBInternalError if it cannot get presentation id 
        """

        triple = [Triple(URI(timeslot), URI(PROPERTY_TIMESLOTPRESENTATION), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            return None
        else:
            return str(result[0][2])

    def get_presentation_title(self, presentation):
        """
        :param presentation: uuid of the presentation

        :return: presentation title in UTF8 or "No title" if it cannot be retrieved
        """

        triple = [Triple(URI(presentation), URI(PROPERTY_PRESENTATIONTITLE), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            sys.stderr.write("ERROR: Can't get presentation title. Setting title = \"No Title\"")
            return "No Title"
        else:
            return str(result[0][2])

    def get_presentation_speaker(self, timeslot):
        """
        Getting presentation speaker's name from his profile
        or timeslot
        
        :param timeslot: uuid of the timeslot

        :return: speaker name in UTF8
        """

        # Try to get speaker's name from profile
        try:
            username = self.get_speaker_name_from_profile(self.get_person_uuid_from_timeslot(timeslot))
            return username
        except Exception as e:
            # Getting speaker's name from timeslot
            username = self.get_username_from_timeslot(timeslot)
        return username

    def get_username_from_timeslot(self, timeslot_uuid):
        """
        :param timeslot_uuid: uuid of the timeslot

        :return: Username in UTF8

        """
        triple = [Triple(URI(timeslot_uuid), URI(PROPERTY_TIMESLOTSPEAKERNAME), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is  False:
            sys.stderr.write('ERROR: Cannot get speaker\'s name from timeslot. Setting name = "No name"')
            return "No Name"
        return self._rdf_result_cp1251_to_utf8(result[0][2])

    def get_speaker_name_from_profile(self, person_uuid):
        """
        :param person_uuid: uuid of the person's profile

        :return: Username in UTF8

        It raise SIBInternalError if it cannot get username from profile    
        """

        triple = [Triple(URI(person_uuid), URI(PROPERTY_NAME), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            sys.stderr.write('ERROR: Cannot get speaker\'s name from profile[{}]\n'.format(str(person_uuid)))
            raise SIBInternalError('ERROR: Cannot get speaker\'s name from profile')
        return self._rdf_result_cp1251_to_utf8(result[0][2])
            
    def get_person_uuid_from_timeslot(self, timeslot_uuid):
        """
        :param timeslot_uuid: uuid of the timeslot

        :return: Person uuid from timeslot

        It raise SIBInternalError if it cannot get username from timeslot
        """

        triple = [Triple(URI(timeslot), URI(PROPERTY_TIMESLOTPERSON), None)]
        result = self.node._rdf_query(triple)
        if self.check_triples(result) is False:
            sys.stderr.write('ERROR: Cannot get speaker\'s UUID from timeslot[{}]\n'.format(str(timeslot_uuid)))
            raise SIBInternalError('ERROR: Cannot get speaker\'s UUID from timeslot')
        return result[0][2]

    def check_triples(self, triples, is_list = True, first = True, second = True, third = True):
        """
        Checking list of triples what is actually triples with non-empty fields

        Keyword arguments:
        is_list -- Is it list or single triple?
        first -- Is first field of the triple required?
        second -- Is second field of the triple required?
        third -- Is third field of the triple required?
        :return: True if it valid list of triples, False otherside.

        """

        if is_list == False:
            return self._check_single_triple(triples, first, second, third)
        else:
            if len(triples) <= 0:
                return False
            for t in triples:
                if self._check_single_triple(t, first, second, third) is False:
                    return False
                
    def _check_single_triple(self, triple, first, second, third):
        length = 0
        if first == True:
            length += 1
        if second == True:
            length += 1
        if third == True:
            length += 1

        if len(triple) < length:
            return False
        else:
            if first is True and (triple[0] is None or triple[0] == ""):
                return False
            if second is True and (triple[1] is None or triple[1] == ""):
                return False
            if third is True and (triple[2] is None or triple[2] == ""):
                return False
        return True

    def _rdf_result_cp1251_to_utf8(self, result):
        """
        Change triple's field encoding from cp1251 to UTF8
        :return: string in UTF-8
        """

        temp = result.value.encode('cp1251')
        temp = temp.decode('1251')
        temp = temp.encode('utf8')
        return temp

class PresentationHandler(KPHandler):
    presentation_uuid = None
    dwa = None

    def __init__(self, node):
        KPHandler.__init__(self, node)
        self.dwa = DiscussionService(DISCUSSION_IP, DISCUSSION_PORT)
    
    def handle(self, added, removed):
        """
            added = [(notification_uuid, startPresentation, presentation_uuid)]
            or
            added = [(notification_uuid, endPresentation, presentation_uuid)]
        """
        
        if len(added) > 0:
            addedSingle = added[0]
            self.presentation_uuid = str(addedSingle[2])
            if str(addedSingle[1]).find("startPresentation") != -1:
                # Presentation was started
                print "Start presentation"
                try:
                    currentTimeslot_uuid = self.get_current_timeslot()
                    self.dwa.setCurrentPresentation(strip_hashtag(currentTimeslot_uuid))
                except Exception as e:
                    sys.stderr.write(error_handler(e))
                except:
                    sys.stderr.write(error_handler())
            elif str(addedSingle[1]).find("endPresentation") != -1:
                print "End Presentation\n\n\n"
                self.dwa.setCurrentPresentation(None)

class ConferenceHandler(KPHandler):
    """
        Actually, it is "SectionHandler", because it works with Sections
    However, it is a handler of the subscription on a "startConference" and "endConference" notifications
    """
    
    dwa = None
    
    section_uuid = None
    section_title = None
    section_date = None

    timeslot_uuids = []
    presentation_titles = []
    presentation_speakers = []
    
    def __init__(self, node):
        KPHandler.__init__(self, node)
        self.dwa = DiscussionService(DISCUSSION_IP, DISCUSSION_PORT)

    def handle(self, added, removed):
        """
        added - list of triples (notificationID, startConference, sectionID), usually one item in list.
        It must work only if added is not empty and removed is empty.
        This method collects some data and calls create() function from "create" module.
        """
        if len(added) > 0:
            try:
                if str(added[0][1]).find("startConference") != -1:
                    print "\n\n\nStart conference\n"
                    if added[0][2] is not None and str(added[0][2]) != "":
                        self.section_uuid = added[0][2]
                        print "Section ID: {}".format(str(self.section_uuid))
                        self.get_section_info(self.section_uuid)
                        self.get_presentation_from_timeslots(self.section_uuid)
                        self.dwa.setCurrentConference(strip_hashtag(self.section_uuid))
                    elif len(removed) <= 0:
                        sys.stderr.write("ERROR: Can't get section ID\nNothing to do here\n\n")

                    print "Creating Disqus threads..."
                    result = self.dwa.createThreads(self.section_title, self.section_date, strip_hashtag(self.section_uuid),
                                         self.timeslot_uuids, self.presentation_titles, self.presentation_speakers)
                    print "Creating threads finished with status:\n\t{}".format(str(result))

                elif str(added[0][1]).find("endConference") != -1:
                    self.dwa.setCurrentConference(None)
                    print "End conference\n\n\n"

            except Exception as e:
                sys.stderr.write(error_handler(e))
            except:
                sys.stderr.write(error_handler())
            finally:
                self._flush_data()
            

    def _flush_data(self):
        self.section_date = None
        self.section_title = None
        self.section_uuid = None

        self.timeslot_uuids = []
        self.presentation_speakers = []
        self.presentation_titles = []

class AggregatorKP(KP):
    def __init__(self, server_ip, server_port):
        KP.__init__(self, str(uuid.uuid4())+"_Aggregator")
        self.ss_handle = ("X",
            (TCPConnector,
            (server_ip,server_port)
            ))

    def join_sib(self):
        self.join(self.ss_handle)

    def leave_sib(self):
        self.CloseSubscribeTransaction(self.st)
        self.leave(self.ss_handle)

    def create_subscription(self, sr_class, sr_property, sr_object, handler):
        try:
            if sr_class is not None:
                sr_class = URI(sr_class)
            
            if sr_property is not None:
                sr_property = URI(sr_property)

            if sr_object is not None:
                sr_object = URI(sr_object)

            trip = [Triple(
                    sr_class,
                    sr_property,
                    sr_object)]
            self.st = self.CreateSubscribeTransaction(self.ss_handle)

            initial_results = self.st.subscribe_rdf(trip, handler)
        except Exception as e:
            sys.stderr.write(error_handler(e))
        except:
            sys.stderr.write("create_subscription error\n")

    def _rdf_query(self, triples):
        qt = self.CreateQueryTransaction(self.ss_handle)
        result = qt.rdf_query(triples)
        self.CloseQueryTransaction(qt)
        return result

def strip_hashtag(token):
    result = (str(token)).split("#")
    if len(result) > 1:
        return result[1]
    else:
        return result[0]

quit = False
pds = []
gp = None

def post_worker(dwa, timeout, kp):
    while True:
        result = dwa.getPosts(timeout)
        # Полученный результа надо как-то передать в agenda
        # Например, создать список троек и воспользоваться
        # kp.insert(triples)
        temp = json.loads(str(result))
        #print temp[result]
        time.sleep(timeout - 1)

def signal_handler(signum, frame):
    quit = True

try:
    pds = [AggregatorKP(SIB_IP, SIB_PORT),
            AggregatorKP(SIB_IP, SIB_PORT),
            AggregatorKP(SIB_IP, SIB_PORT),
            AggregatorKP(SIB_IP, SIB_PORT)
        ]

    for pd in pds:
        pd.join_sib()

    #gp = Process(target=post_worker, args=(DiscussionService(DISCUSSION_IP, DISCUSSION_PORT),
    #                                        60, AggregatorKP(SIB_IP, SIB_PORT)))
    #gp.start()

    pds[0].create_subscription(None, PROPERTY_STARTCONFERENCE, None, ConferenceHandler(pds[0]))
    pds[1].create_subscription(None, PROPERTY_ENDCONFERENCE, None, ConferenceHandler(pds[1]))
    pds[2].create_subscription(None, PROPERTY_STARTPRESENTATION, None, PresentationHandler(pds[2]))
    pds[3].create_subscription(None, PROPERTY_ENDPRESENTATION, None, PresentationHandler(pds[3]))
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
except Exception as e:
    sys.stderr.write(error_handler(e))

print "Subscription:\t\t\t Success"

while True:
    i = raw_input('\nType "exit" to exit the program\n')

    if i.lower() == "exit" or quit:
        break

for pd in pds:
    pd.leave_sib()

#gp.terminate()
