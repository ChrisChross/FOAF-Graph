import streamlit as st
# from analysis import GraphAlgos
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config, GraphAlgos
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Set

###############################
###### DATA FOR PERSONS #######
###############################

def get_people():
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  query_string = """  select DISTINCT ?person ?label where {
                                            ?person rdf:type dbo:Person.
                                            ?person rdfs:label ?label.
                                          }
                 """

  sparql.setQuery(query_string)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  persons = set()
  persons.add("")
  for result in results["results"]["bindings"]:
    person = result["person"]["value"].rsplit("/",1)[1]
    persons.add(person)
  return persons


def load_persons(recource, store:TripleStore=None):

  if store == None:
    store = TripleStore()

  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  # queryString = "SELECT * WHERE { ?s ?p ?o. }"
  target = f"<http://dbpedia.org/resource/{recource}>"
  query_string = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " \
                  "PREFIX dbo: <http://dbpedia.org/ontology/>"  \
                  "SELECT ?label ?birthPlace ?birthDate ?deathDate ?picture ?abstract " \
                  f"WHERE {{ {target} " \
                                                            "rdfs:label ?label ." \
                                                            f"OPTIONAL {{ {target} " \
                                                            "dbo:birthPlace ?birthPlace;" \
                                                            "dbo:birthDate ?birthDate;" \
                                                            "dbo:deathDate ?deathDate;" \
                                                            "dbo:abstract ?abstract;" \
                                                            "dbo:thumbnail ?picture ." \
                                                            "}" \
        "filter langMatches( lang(?label), 'EN' ) }" \
        "LIMIT 1"
  # st.write(query_string)
  sparql.setQuery(query_string)
  # sparql = SPARQLWrapper("http://dbpedia.org/sparql/resource/Asturias")
  # sparql.setReturnFormat(N3)
  sparql.setReturnFormat(JSON)
 #  sparql.setQuery(queryString)
  results = sparql.query().convert()
  abstract = ""
  picture = ""
  for result in results["results"]["bindings"]:
    subj = result["label"]["value"]
    if "picture" in result:
      picture = result["picture"]["value"]
    if "abstract" in result:
      abstract = result["abstract"]["value"]
    # pic, picture = circle_image(picture, size=(300, 300))
    for label in result:
      if not label == "picture" and not label == subj and not label == "abstract":
        pred = label
        if "http://dbpedia.org/resource/" in result[label]["value"]:
          obj = result[label]["value"].rsplit("/", 1)[1]
        else:
          obj = result[label]["value"]
        # st.write(subj, pred, obj)
        store.add_triple(subj, pred, obj, picture)
  return store, abstract

class PersonsService:
  store: TripleStore
  algos: GraphAlgos
  node_names: List
  loaded: bool

@st.cache(allow_output_mutation=True)
def state():
    perservice = PersonsService()
    perservice.loaded = False
    return perservice
