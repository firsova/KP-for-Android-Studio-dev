# -*- coding: utf-8 -*-

import urllib
import datetime
import os, os.path
import sys
import uuid
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from disqusapi import DisqusAPI
from disqusapi import APIError
from disqusdb.DisqusDB import DisqusDB
from config import *
from exception_handler import *

DEBUG_MSG = "\nDEBUG ({}):".format(os.path.basename(__file__))

class Disqus(object):

    THREAD_MESSAGE_LENGTH = 402
    THREAD_TITLE_LENGTH = 64
    SEPARATOR = "##:!:##"

    def __init__(self):
        if not ACCESS_TOKEN:
            sys.exit("Access_token value is required\n")
        if not SECRET_KEY:
            sys.exit("Secret_key value is required\n")
        if not PUBLIC_KEY:
            sys.exit("Public_key value is required\n")
        if not FORUM:
            sys.exit("Forum name is required\n")

        self.access_token = ACCESS_TOKEN
        self.secret_key = SECRET_KEY
        self.public_key = PUBLIC_KEY
        self.forum = FORUM
        self.disqus = DisqusAPI(self.secret_key, self.public_key)
        self.disqus_db = DisqusDB()

    '''
        Creates a category and threads on Disqus.com for the current section
    '''
    def create_threads(self, sectionTitle, sectionDate, sectionUUID, timeslotUUIDs, presentationTitles, speakers):
        try:
            if not timeslotUUIDs:
                raise Exception("timeslotUUIDs array is empty")
            if not presentationTitles:
                raise Exception("presentationTitles array is empty")
            if not (len(timeslotUUIDs) == len(presentationTitles) and len(presentationTitles) == len(speakers)):
                raise Exception("Arguments arrays have different length")

            # Synchronizing DB with Disqus.com
            synch_result = "Synchronization with Disqus.com was not performed\n"
            if ALLOW_SYNCH:
                synch_result = self.synch_disqus()

            errors = 0
            error_messages = ""

            # Creating category
            sectionDate_quoted = urllib.quote(sectionDate)

            '''
            Checks if there is already a category with sectionUUID. 
            If so, the new category won't be created and presentations will be added to the existing category.
            '''
            category_old = self.disqus_db.get_category_from_db(sectionUUID)
            
            if not category_old:
                category = self.disqus.disqus.get('categories.create', **{"method":"POST", "forum":self.forum, "title":sectionDate_quoted, 
                    "default":0, "access_token":self.access_token})
                category_id = category.get("id").encode("utf-8")
                self.disqus_db.add_category_to_db(category_id, sectionUUID, sectionTitle)
            else:
                category_id = str(category_old)

            # Creating presentations discussion threads
            for i in range(len(timeslotUUIDs)):

                threadTitle = presentationTitles[i] + " " + speakers[i]
                threadTitle_cut_quoted = threadTitle

                threadIdent = timeslotUUIDs[i]
                threadIdent_quoted = urllib.quote(timeslotUUIDs[i])
                try:
                    thread = self.disqus.disqus.get('threads.create', **{"method":"POST", "forum":self.forum, "category":category_id, 
                        "title":threadTitle_cut_quoted, "identifier":threadIdent_quoted, 
                        "access_token":self.access_token})
                    self.disqus_db.add_thread_to_db(thread.get("id"), thread.get("category"), threadIdent, presentationTitles[i], speakers[i])
                    thread_id = thread.get("id").encode("utf-8")
                    threadMessage = category_id + Disqus.SEPARATOR \
                                    + sectionUUID + Disqus.SEPARATOR \
                                    + sectionTitle + Disqus.SEPARATOR \
                                    + thread_id + Disqus.SEPARATOR \
                                    + threadIdent + Disqus.SEPARATOR \
                                    + presentationTitles[i] + Disqus.SEPARATOR \
                                    + speakers[i]
                    threadMessage_quoted = urllib.quote(threadMessage)
                    thread = self.disqus.disqus.get('threads.update', **{"method":"POST", "thread":thread.get("id"), 
                        "message": threadMessage_quoted, "access_token":self.access_token})
                except Exception as e:
                    errors = errors + 1
                    error_messages += "\t" + str(e) + "\n"
                    pass

            if not category_old:
                # Creating organization thread
                orgThreadTitle = ORGANIZATION_THREAD_TITLE
                orgThreadSpeaker = ORGANIZATION_THREAD_SPEAKER

                tempStr = str(uuid.uuid4()) + "_org"
                orgThreadIdent = urllib.quote(tempStr)
                thread = self.disqus.disqus.get('threads.create', **{"method":"POST", "forum":self.forum, "category":category_id, 
                    "title":orgThreadTitle, "identifier":orgThreadIdent, "access_token":self.access_token})
                self.disqus_db.add_thread_to_db(thread.get("id"), thread.get("category"), orgThreadIdent, orgThreadTitle, orgThreadSpeaker)

                thread_id = thread.get("id").encode("utf-8")
                orgThreadMessage = category_id + Disqus.SEPARATOR \
                                    + sectionUUID + Disqus.SEPARATOR \
                                    + sectionTitle + Disqus.SEPARATOR \
                                    + thread_id + Disqus.SEPARATOR \
                                    + orgThreadIdent + Disqus.SEPARATOR \
                                    + orgThreadTitle + Disqus.SEPARATOR \
                                    + orgThreadSpeaker
                orgThreadMessage_quoted = urllib.quote(orgThreadMessage)
                thread = self.disqus.disqus.get('threads.update', **{"method":"POST", "thread":thread.get("id"), 
                    "message": orgThreadMessage_quoted, "access_token":self.access_token})

            print DEBUG_MSG + "{}:".format(sys._getframe().f_code.co_name) + synch_result + \
                "Process finished at {} with {} errors\n".format(str(datetime.datetime.now()), str(errors)) + error_messages
            return synch_result + "\tProcess finished at {} with {} errors\n".format(str(datetime.datetime.now()), str(errors)) + error_messages
        except APIError as e:
            sys.stderr.write('\nCannot create thread {}: {}: {}\n'.format(threadIdent, str(e.code), e.message))
            pass
        except Exception as e:
            sys.stderr.write(error_handler(e))
            raise e
        except:
            sys.stderr.write(error_handler())
            raise

    '''
        This function is not needed anymore but here it is.
    '''
    def cut_utf8_string(self, string, byte_length):
        cut = False
        while True:
            in_bytes = bytearray(string)
            if len(in_bytes) >= byte_length - 2:
                string = string[:len(string) - 1]
                cut = True
            else:
                if cut:
                    string = string + '..'
                return string

    '''
        Does synchronization with Disqus.com: just deletes all entries in 'category' and 
        'thread' tables in the DB and fills them again with data stores at Disqus.com
    '''
    def synch_disqus(self, force = False):
        try:
            if not force:
                rows_count = self.disqus_db.get_rows_count()
                if rows_count > 0:
                    print DEBUG_MSG + "{}: Synch is not needed.\n".format(sys._getframe().f_code.co_name)
                    return "Synch is not needed.\n"

            cursor = None
            cursorNext = None
            cursorMore = True

            # 'category': category_id int, section_uuid text, section_title text
            # 'thread': thread_id integer, category_id integer, identifier text, presentation_title text, speaker_name text
            c = 0
            self.disqus_db.delete_all_from_tables()
            while cursorMore:
                c += 1
                if cursorNext:
                    threads = self.disqus.disqus.get('threads.list', **{"method":"GET", "forum":self.forum, "cursor": cursorNext})
                else:
                    threads = self.disqus.disqus.get('threads.list', **{"method":"GET", "forum":self.forum})
                cursor = threads.cursor
                cursorMore = cursor.get("more")
                cursorNext = cursor.get("id")
                for thread in threads:
                    threadMessage = thread.get("message").encode("utf-8")
                    threadMessage_unquoted = urllib.unquote(threadMessage)
                    messageValues = threadMessage_unquoted.split(Disqus.SEPARATOR)
                    if len(messageValues) == 7:
                        # Message is wrapped in <p> </p> tags so removing them is neeeded
                        category_id = int(messageValues[0][3:])
                        sectionUUID = messageValues[1]
                        sectionTitle = messageValues[2] 
                        thread_id = int(messageValues[3])
                        threadIdent = messageValues[4]
                        presentationTitle = messageValues[5]
                        speaker = messageValues[6][:-4]
                    self.disqus_db.add_thread_to_db(thread_id, category_id, threadIdent, presentationTitle, speaker)
                    self.disqus_db.add_category_to_db(category_id, sectionUUID, sectionTitle)

            print DEBUG_MSG + "{}: Successfully synchronized DB with Disqus.com.\n".format(sys._getframe().f_code.co_name)
            return "Successfully synchronized DB with Disqus.com. Cursors: " + str(c) + "\n"
        except Exception as e:
            sys.stderr.write(error_handler(e))
            raise e
        except:
            sys.stderr.write(error_handler())
            raise

    '''
    Retrieves posts on the current discussion created up to 'sinceSeconds' seconds ago.
    '''
    def get_posts(self, sinceSeconds):
        try:
            event = self.disqus_db.get_current_event()
            result = []
            
            if not event:
                print DEBUG_MSG + "{}: No event\n".format(sys._getframe().f_code.co_name)
                return json.dumps({"result":result})
            section_uuid, identifier = event
            if not identifier:
                print DEBUG_MSG + "{}: No identifier\n".format(sys._getframe().f_code.co_name)
                return json.dumps({"result":result})

            sinceTimeLocal = datetime.datetime.now() - datetime.timedelta(seconds = sinceSeconds)
            sinceTimeUTC = self.local_to_UTC(sinceTimeLocal)

            cursor = None
            cursorNext = None
            cursorMore = True
            posts = []
            while cursorMore:
                if cursorNext:
                    posts = self.disqus.disqus.get('threads.listPosts', **{"method":"GET", "forum":self.forum, "cursor": cursorNext,
                        "since": sinceTimeUTC, "thread:ident":identifier, "order":"asc"})
                else:
                    posts = self.disqus.disqus.get('threads.listPosts', **{"method":"GET", "forum":self.forum,
                        "since": sinceTimeUTC, "thread:ident":identifier, "order":"asc"})
                cursor = posts.cursor
                cursorMore = cursor.get("more")
                cursorNext = cursor.get("id")
                if posts:
                    for post in posts:
                        author = post.get("author").get("name").encode("utf-8")
                        message = post.get("raw_message").encode("utf-8")
                        result.append({"name":author, "message":message})
            print DEBUG_MSG + "{}: Retrieved recent posts from Disqus.com\n".format(sys._getframe().f_code.co_name)
            return json.dumps({"result":result})
        except Exception as e:
            sys.stderr.write(error_handler(e))
            raise e
        except:
            sys.stderr.write(error_handler())
            raise

    '''
        Converts a timestamp in local time to a timestamp in UTC
    '''
    def local_to_UTC(self, local):
        try:
            TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
            local = local.strftime(TIME_FORMAT)
            timestamp =  str(time.mktime(datetime.datetime.strptime(local, TIME_FORMAT).timetuple()) )[:-2]
            utc = datetime.datetime.utcfromtimestamp(int(timestamp))
            return utc
        except Exception as e:
            raise e