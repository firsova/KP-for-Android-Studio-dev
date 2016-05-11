from smart_m3.m3_kp import *
from ontology import *
import uuid
import re

def _generate_uri():
    return (NS_SMARTROOM + str(uuid.uuid4()))[:45]

class WebPageProcessor(KP):
    def __init__(self, sib_ip="127.0.0.1", sib_port=10010, kp_name="Web_page-service"):
        KP.__init__(self, kp_name)
        self.ss_handle = ("X", (TCPConnector, (sib_ip,
                                               sib_port)))
    
    def join_sib(self):
        self.join(self.ss_handle)

    def leave_sib(self):
        self.leave(self.ss_handle)
    
    def publish_vote_result(self, placeslot_uuid, person_uuid, vote):
        person_uuid = NS_SMARTROOM + person_uuid
        
        if vote == "1":
            triples = [Triple(URI(placeslot_uuid), URI(PROPERTY_PLACESLOTPLUSRATING), URI(person_uuid))]
        elif vote == "-1":
            triples = [Triple(URI(placeslot_uuid), URI(PROPERTY_PLACESLOTMINUSRATING), URI(person_uuid))]
            
        rem_triple = [Triple(URI(placeslot_uuid), URI(PROPERTY_PLACESLOTPLUSRATING), URI(person_uuid)),
                      Triple(URI(placeslot_uuid), URI(PROPERTY_PLACESLOTMINUSRATING), URI(person_uuid))]
                      
        self._update_triples(triples, rem_triple)
    
    def notification_voteUpdate(self, placeslot_uuid):
        notification_uuid = self._generate_uri() 
        triples = [Triple(URI(notification_uuid), URI(RDF_TYPE), URI(CLASS_SOCIALPROGRAMNOTIFICATION)),
                Triple(URI(notification_uuid), URI(PROPERTY_VOTEUPDATE), URI(placeslot_uuid))]
        print triples;
        self._insert_triples(triples)
        
    def publish_service_urls(self, url):
        socialprogramservice_uuid = self.get_social_program_service_uuid()
        if socialprogramservice_uuid == "" or socialprogramservice_uuid == None:
            print "Social program service is not found"
            return
        triples = [Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASCLIENTURL), Literal(url+"/client")),
                    Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASAGENDASERVICEURL), Literal(url+"/agenda")),
                    Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASPRESENTATIONSERVICEURL), Literal(url+"/presentation"))]
        rem_triple = [Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASCLIENTURL), None),
                    Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASCLIENTURL), None),
                    Triple(URI(socialprogramservice_uuid), URI(PROPERTY_HASCLIENTURL), None)]
        self._update_triples(triples, rem_triple)
    
    def get_social_program_service_uuid(self):
        query = """SELECT ?socialprogramservice
                   WHERE {{ ?socialprogramservice rdf:type <{0}> }}"""
        query = query.format(CLASS_SOCIALPROGRAMSERVICE)       
        query_result = self._sparql_query(query)
        for result in query_result:
            for property in result:
                if property[0] == "socialprogramservice":
                    return property[2]
                else:
                    return ""
    

    def _insert_triples(self, triples):
        ins = self.CreateInsertTransaction(self.ss_handle)
        ins.send(triples, confirm = True)
        self.CloseInsertTransaction(ins)
        
    def _update_triples(self, triples_ins, triples_rem):
        upd = self.CreateUpdateTransaction(self.ss_handle)
        upd.update(triples_ins, "RDF-M3", triples_rem, "RDF-M3", confirm = True)
        self.CloseUpdateTransaction(upd)

    def _remove_triples(self, triples):
        rem = self.CreateRemoveTransaction(self.ss_handle)
        rem.remove(triples)
        self.CloseRemoveTransaction(rem)
    
    def _rdf_query(self, triples):
        qt = self.CreateQueryTransaction(self.ss_handle)
        result = qt.rdf_query(triples)
        self.CloseQueryTransaction(qt)
        
        return result
    
    def _sparql_query(self, sparql):
        PREFIXES = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/02/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            """
        q = PREFIXES+sparql

        qt = self.CreateQueryTransaction(self.ss_handle)
        result = qt.sparql_query(q)
        self.CloseQueryTransaction(qt)

        return result
   
    def _generate_uri(self):
        return (NS_SMARTROOM + str(uuid.uuid4()))[:45]
    
    def getAllTriples(self, limit=None):
        sparql = """SELECT ?s ?p ?o WHERE {
                    ?s ?p ?o }
            """
        if limit:
            sparql += "LIMIT " + str(limit)
        return self._sparql_query(sparql)
