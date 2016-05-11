from smart_m3.m3_kp import *
from ontology import *
import uuid
import re
from exception_handler import *

class WebPageProcessor(KP):
    def __init__(self, sib_ip="127.0.0.1", sib_port=10010, kp_name="Discussion-service"):
        KP.__init__(self, kp_name)
        self.ss_handle = ("X", (TCPConnector, (sib_ip,
                                               sib_port)))

    def publish_service_urls(self, url):
        try:
            discussion_service_uuid = NS_SMARTROOM + "discussion-service"
            triples = [Triple(URI(discussion_service_uuid), URI(RDF_TYPE), URI(CLASS_DISCUSSIONSERVICE)),
                Triple(URI(discussion_service_uuid), URI(PROPERTY_HASCLIENTURL), Literal(url))]
            rem_triple = [Triple(URI(discussion_service_uuid), None, None)]
            self._update_triples(triples, rem_triple)
            return "Service URL={} was published".format(url)
        except Exception as e:
            return error_handler(e)

    def _update_triples(self, triples_ins, triples_rem):
        upd = self.CreateUpdateTransaction(self.ss_handle)
        upd.update(triples_ins, "RDF-M3", triples_rem, "RDF-M3", confirm = True)
        self.CloseUpdateTransaction(upd)