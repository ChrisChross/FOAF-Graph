from dataclasses import dataclass

import streamlit as st
from analysis import GraphAlgos
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Set

###############################
### DATA FOR INSPIRATIONALS ###
###############################

def get_inspired():
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")

  query_string = """
  SELECT ?name_pe1_en ?rel_en ?name_pe2_en
  WHERE {
    {
         SELECT ?name_p1 ?rel ?name_p2
         WHERE {
             ?p1 a foaf:Person .
             ?p1 dbo:influencedBy ?p2 .
             ?p2 a foaf:Person .
             ?p1 foaf:name ?name_p1 .
             ?p2 foaf:name ?name_p2 .
            dbo:influencedBy rdfs:label ?rel .
            }
         LIMIT 100
    }
    UNION
    {
         SELECT ?name_p1 ?rel ?name_p2
         WHERE {
            ?p1 a foaf:Person .
            ?p1 dbo:influenced ?p2 .
            ?p2 a foaf:Person .
            ?p1 foaf:name ?name_p1 .
            ?p2 foaf:name ?name_p2 .
            dbo:influenced rdfs:label ?rel .
        }
     LIMIT 100
    }
    FILTER ( LANG(?name_p1) = "en" && LANG(?rel) = "en" && LANG(?name_p2) = "en" )
    BIND ( STR(?name_p1) AS ?name_pe1_en )
    BIND ( STR(?rel) AS ?rel_en )
    BIND ( STR(?name_p2) AS ?name_pe2_en )
  }
  """

  sparql.setQuery(query_string)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  store = TripleStore()
  for result in results["results"]["bindings"]:
    node1 = result["name_pe1_en"]["value"]
    link = result["rel_en"]["value"]
    node2 = result["name_pe2_en"]["value"]
    store.add_triple(node1, link, node2)
  return store

def load_data():
  store = get_inspired()
  algos = GraphAlgos(store)
  node_names = [n.id for n in store.nodes_set]
  return store, algos, node_names

class InspService:
  store: TripleStore
  algos: GraphAlgos
  node_names: List
  loaded: bool

@st.cache(allow_output_mutation=True)
def state():
    inspService = InspService()
    inspService.loaded = False
    return inspService
