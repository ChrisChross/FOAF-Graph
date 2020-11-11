import streamlit as st
from SPARQLWrapper import SPARQLWrapper, N3, JSON, JSONLD, TURTLE, CSV
from rdflib import Graph
# graph analysis library
from streamlit_agraph import agraph, Node, Edge, Config
from typing import List,Set
from layout import footer

class Triple:
  def __init__(self, subj: Node, pred: Edge, obj:Node ) -> None:
    self.subj = subj
    self.pred = pred
    self.obj = obj

class TripleStore:
  def __init__(self) ->None:
    self.nodes_set: Set[Node] = set()
    self.edges_set: Set[Edge] = set()
    self.triples_set: Set[Triple] = set()

  def add_triple(self, node1, link, node2, picture=""):
    nodeA = Node(node1, svg=picture)
    nodeB = Node(node2)
    edge = Edge(source=nodeA.id, target=nodeB.id, labelProperty=link, renderLabel=True)  # linkValue=link
    triple = Triple(nodeA, edge, nodeB)
    self.nodes_set.update([nodeA, nodeB])
    self.edges_set.add(edge)
    self.triples_set.add(triple)

  def getTriples(self)->Set[Triple]:
    return self.triple_set

  def getNodes(self)->Set[Node]:
    return self.nodes_set

  def getEdges(self)->Set[Edge]:
    return self.edges_set

# http://dbpedia.org/snorql/

def get_foafs():
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  query_string = """  SELECT ?p1 ?rel ?p2 WHERE {
                                                  {
                                                    ?p1 a foaf:Person .
                                                    ?p1 ?rel ?p2 .
                                                    ?p2 a foaf:Person .
                                                    }
                                                    UNION
                                                    {
                                                    ?p2 a foaf:Person .
                                                    ?p2 ?rel ?p1 .
                                                    ?p1 a foaf:Person .
                                                  }

                                                }
                                                LIMIT 400
                 """
  sparql.setQuery(query_string)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  # st.write(results)
  store = TripleStore()
  for result in results["results"]["bindings"]:
    node1 = result["p1"]["value"].rsplit('/', 1)[1]
    link = result["rel"]["value"].rsplit('/', 1)[1]
    node2 = result["p2"]["value"].rsplit('/', 1)[1]
    store.add_triple(node1,link,node2)
  return store
  #persons = []
  #for result in results["results"]["bindings"]:
  #  person = result["person"]["value"]
  #  persons.append(person)
  #return persons

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
  # sparql_endpoint = st.sidebar.text_input("SPARQL ENDPOINT: ", "http://dbpedia.org/sparql")
  query_type = st.sidebar.selectbox("Quey Tpye: ", ["Person", "FOAF"]) #rdfs:Resource , "Company", "Location"
  # resource_name = st.sidebar.text_input("Quey Tpye: ", "Barack_Obama" )
  config = Config(height=500, width=700, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True,
                  collapsible=True)
  # get_foafs()
  if query_type == "Person":
    st.subheader("Person (Date of birth and place)")
    persons = list(get_people())
    st.write(len(persons))
    chosen_person = st.sidebar.selectbox("Choose a Person: ", persons)
    nodes, edges = do_query(chosen_person)
    agraph(nodes, edges, config)
  if query_type=="FOAF":
    st.subheader("Friend-of-a-friend")
    with st.spinner("Loading data"):
      store = get_foafs()
      st.write(len(store.getNodes()))
    st.success("Done")
    agraph(list(store.getNodes()), (store.getEdges() ), config)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()

