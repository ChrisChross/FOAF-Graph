import streamlit as st
from typing import List,Set
from SPARQLWrapper import SPARQLWrapper, JSON
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config

from services.PersService import get_people

def app():
  st.subheader("Person (Date of birth and place)")
  persons = list(get_people())
  st.write(len(persons))

  chosen_person = st.sidebar.selectbox("Choose a Person: ", persons)
  config = Config(height=500, width=700, nodeHighlightBehavior=True,
                  highlightColor="#F7A7A6", directed=True, collapsible=True)
  if chosen_person != "":
    store, abstract = get_people(chosen_person)
    agraph(list(store.getNodes()), (store.getEdges()), config)
    st.write(abstract)
