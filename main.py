import streamlit as st
from SPARQLWrapper import SPARQLWrapper, N3, JSON, JSONLD, TURTLE, CSV
from rdflib import Graph
# graph analysis library
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from typing import List,Set
from layout import footer
from image import circle_image
import os

# http://dbpedia.org/snorql/

def file_selector(folder_path='.'):
  filenames = os.listdir(folder_path)
  selected_filename = st.selectbox('Select a file', filenames, key="unique")
  return os.path.join(folder_path, selected_filename)


filename = file_selector()
st.write('You selected `%s`' % filename)
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
  for result in results["results"]["bindings"]:
    person = result["person"]["value"].rsplit("/",1)[1]
    persons.add(person)
  return persons

def do_query(recource):

  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  # queryString = "SELECT * WHERE { ?s ?p ?o. }"

  query_string = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " \
                  "PREFIX dbo: <http://dbpedia.org/ontology/>"  \
                  "SELECT ?label ?birthPlace ?birthDate ?picture " \
                  f"WHERE {{ <http://dbpedia.org/resource/{recource}> " \
                                                            "rdfs:label ?label;" \
                                                            "dbo:birthPlace ?birthPlace;" \
                                                            "dbo:birthDate ?birthDate;" \
                                                            "dbo:thumbnail ?picture ." \
        "filter langMatches( lang(?label), 'EN' ) }" \
        "LIMIT 1"
  # st.write(query_string)
  sparql.setQuery(query_string)
  # sparql = SPARQLWrapper("http://dbpedia.org/sparql/resource/Asturias")
  # sparql.setReturnFormat(N3)
  sparql.setReturnFormat(JSON)
 #  sparql.setQuery(queryString)
  results = sparql.query().convert()

  store = TripleStore()

  for result in results["results"]["bindings"]:
    subj = result["label"]["value"]
    picture = result["picture"]["value"]
    picture = circle_image(picture, size=(300, 300))
    for label in result:
      if not label == "picture" and not label ==subj:
        pred = label
        if "http://dbpedia.org/resource/" in result[label]["value"]:
          obj = result[label]["value"].rsplit("/", 1)[1]
        else:
          obj = result[label]["value"]
        # st.write(subj, pred, obj)
        store.add_triple(subj, pred, obj, picture)
  return list(store.nodes_set), list(store.edges_set)


def app():
  footer()
  st.title("Graph Example")
  st.sidebar.title("Welcome")
  filename = file_selector()
  st.write('You selected `%s`' % filename)
  # sparql_endpoint = st.sidebar.text_input("SPARQL ENDPOINT: ", "http://dbpedia.org/sparql")
  query_type = st.sidebar.selectbox("Quey Tpye: ", ["Person", "Inspirationals"]) #rdfs:Resource , "Company", "Location"
  # resource_name = st.sidebar.text_input("Quey Tpye: ", "Barack_Obama" )
  config = Config(height=500, width=700, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True,
                  collapsible=True)
  if query_type == "Person":
    st.subheader("Person (Date of birth and place)")
    persons = list(get_people())
    st.write(len(persons))
    chosen_person = st.sidebar.selectbox("Choose a Person: ", persons)
    nodes, edges = do_query(chosen_person)
    agraph(nodes, edges, config)
  if query_type=="FOAF":
    st.subheader("Inspirationals")
    with st.spinner("Loading data"):
      store = get_inspired()
      st.write(len(store.getNodes()))
    st.success("Done")
    agraph(list(store.getNodes()), (store.getEdges() ), config)

if __name__ == '__main__':
    app()

