from DiscussionService import *
import datetime

IP = "127.0.0.1"
PORT = "80"

if __name__ == "__main__":
    ds = DiscussionService(IP, PORT)
    
    ds.setCurrentConference("test_section_" + str(datetime.datetime.now()))
    
    ds.setCurrentPresentation("test_presentation_" + str(datetime.datetime.now()))
    ds.setCurrentPresentation(None)

    ds.setCurrentConference(None)
    
    ds.createThreads("test section", "today_" + str(datetime.datetime.now()), "test_section_" + str(datetime.datetime.now()),
                        ["test_timeslot_" + str(datetime.datetime.now()), "test_timeslot_1" + str(datetime.datetime.now())], 
                        ["test_presentation_" + str(datetime.datetime.now()), "test_presentation_1" + str(datetime.datetime.now())],
                        ["test_speaker_" + str(datetime.datetime.now()), "test_speaker_1" + str(datetime.datetime.now())])
