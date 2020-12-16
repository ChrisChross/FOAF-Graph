import streamlit as st
from typing import List,Set
from SPARQLWrapper import SPARQLWrapper, JSON
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config

from services import PersService

def app():
  persState = PersService.state()
  st.subheader("Person (Date of birth and place)")
  st.markdown("---")
  if not persState.loaded:
    st.write("Please load data in the Data Management Page first.")
    node_names = []
  else:
    store = persState.store
    algos = persState.algos
    node_names = persState.node_names

  persons = list(PersService.get_people())
  st.write(len(persons))

  chosen_person = st.sidebar.selectbox("Choose a Person: ", persons)

  config = Config(height=500, width=700, nodeHighlightBehavior=True,
                  highlightColor="#F7A7A6", directed=True, collapsible=True)
  if chosen_person != "":
    store, abstract = PersService.load_persons(chosen_person)
    agraph(list(store.getNodes()), (store.getEdges()), config)
    st.write(abstract)
