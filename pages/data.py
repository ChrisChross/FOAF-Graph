
import streamlit as st
from analysis import GraphAlgos
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
from SPARQLWrapper import SPARQLWrapper, JSON
from services import InspService, PersService
import pandas as pd

def app():
  inspState = InspService.state()
  if st.button("Load Inspirationals"):
    with st.spinner("Loading data"):
      inspState.store, inspState.algos, inspState.node_names = InspService.load_data()
      inspState.loaded = True
      st.write("Nodes loaded: " + str(len(inspState.store.getNodes())))
      st.success("Done")
  if st.button("Load Persons"):
    persState = PersService.state()
    with st.spinner("Loading data"):
      persState.store, persState.algos, persState.node_names = PersService.load_persons()
  if hasattr(inspState, "store"):
    triples = inspState.store.getTriples()
    data_table = [[triple.subj.id, triple.pred.labelProperty, triple.obj.id] for triple in triples]
    df = pd.DataFrame(data=data_table,columns=["Sub_id", "label", "obj_id"])
    st.table(df)

    #st.write()
