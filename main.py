import streamlit as st
from typing import List, Set
from SPARQLWrapper import SPARQLWrapper, N3, JSON, JSONLD, TURTLE, CSV

from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from pages import data, persons, inspirationals

from analysis import GraphAlgos
from layout import footer
from image import circle_image


# http://dbpedia.org/snorql/


PAGES = {
    "Data Management": data,
    "Persons": persons,
    "Inspirationals": inspirationals
}

def app():
    st.set_page_config(page_title='Agraph', page_icon=":fairy:")
    footer()
    st.title("Interactive Graph Component")
    st.markdown("---")
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()
#
# def app():
#   # st.set_page_config(layout="wide")
#   #footer()
#   #st.title("Interactive Graph Component")
#   #st.title("Graph Example")
#   #st.sidebar.title("Welcome")
#   # sparql_endpoint = st.sidebar.text_input("SPARQL ENDPOINT: ", "http://dbpedia.org/sparql")
#   # query_type = st.sidebar.selectbox("Quey Tpye: ", ["Person", "Inspirationals"], key="second") #rdfs:Resource , "Company", "Location"
#   # resource_name = st.sidebar.text_input("Quey Tpye: ", "Barack_Obama" )
#   config = Config(height=500, width=700, nodeHighlightBehavior=True, highlightColor="#F7A7A6", directed=True,
#                   collapsible=True)
#
#
#   if query_type == "Person":
#     st.subheader("Person (Date of birth and place)")
#     persons = list(get_people())
#     st.write(len(persons))
#     chosen_person = st.sidebar.selectbox("Choose a Person: ", persons)
#     if chosen_person != "":
#       store, abstract = do_query(chosen_person)
#       agraph(list(store.getNodes()), (store.getEdges() ), config)
#       st.write(abstract)
#
#   if query_type=="Inspirationals":
#     st.subheader("Inspirationals")
#     session_state = SessionState.get(store=None, algos=None, node_names=[], checkboxed=False)
#     if not session_state.checkboxed:
#       store, algos, node_names = load_data()
#       session_state.store = store
#       session_state.algos = algos
#       session_state.node_names = node_names
#       session_state.checkboxed = True
#     else:
#       store = session_state.store
#       algos = session_state.algos
#       node_names = session_state.node_names
#     if len(node_names) > 0:
#       algo_type = st.sidebar.selectbox("Algo ", ["", "Shortest Path", "Community", "PageRank"], key="second")
#       chosen_person_a = st.sidebar.selectbox("Choose Person A: ", node_names, key="p1")
#       chosen_person_b = st.sidebar.selectbox("Choose Person B: ", node_names, key="p2")
#       if algo_type == "Shortest Path":
#         # node_names = [n.id for n in store.nodes_set]
#         if chosen_person_a != "" and chosen_person_b != "" and chosen_person_a != chosen_person_b :
#           analysis_results = algos.shortest_path(chosen_person_a, chosen_person_b)
#           sp_store = TripleStore()
#           if len(analysis_results) > 0:
#             for idx, connection in enumerate(analysis_results):
#               n1 = connection.replace(" ", "_")
#               if idx+1 < len(analysis_results):
#                 n2 = analysis_results[idx + 1]
#                 sp_store.add_triple(connection, "knows", n2, "")
#               sp_store, _ = do_query(n1, sp_store)
#             agraph(list(sp_store.getNodes()), (sp_store.getEdges()), config)
#           else:
#             st.write("None connections found. Try something else.")
#         else:
#           st.write("Choose choose different persons first.")
#       else:
#           agraph(list(store.getNodes()), (store.getEdges()), config)

if __name__ == '__main__':
    app()

