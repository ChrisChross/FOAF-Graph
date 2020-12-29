import streamlit as st
from typing import List,Set
from SPARQLWrapper import SPARQLWrapper
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config

from services.InspService import load_data
from services.PersService import load_persons
<<<<<<< HEAD
import SessionState
=======

>>>>>>> 6f6a9624da414e66674de21213f6c8f387db8519
from services import InspService

def app():
  inspState = InspService.state()
  st.subheader("Inspirationals")
  st.markdown("---")
<<<<<<< HEAD
  session_state = SessionState.get(store=None, algos=None, node_names=[], checkboxed=False)
  if not inspState.loaded:
    st.write("Please load data in the Data Management Page first.")
    node_names = []
    # store, algos, node_names = load_data()
    # session_state.store = store
    # session_state.algos = algos
    # session_state.node_names = node_names
    # session_state.checkboxed = True
=======
  if not inspState.loaded:
    st.write("Please load data in the Data Management Page first.")
    node_names = []
>>>>>>> 6f6a9624da414e66674de21213f6c8f387db8519
  else:
    store = inspState.store
    algos = inspState.algos
    node_names = inspState.node_names
  if len(node_names) > 0:
    chosen_person_a = st.sidebar.selectbox("Choose Person A: ", node_names, key="p1")
    chosen_person_b = st.sidebar.selectbox("Choose Person B: ", node_names, key="p2")
    algo_type = st.sidebar.selectbox("Algo ", ["", "Shortest Path", "Community", "PageRank"], key="second")
<<<<<<< HEAD
    config = Config(height=500, width=700, nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6", directed=True, collapsible=True)
=======
    config = Config(height=500,
                    width=700,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6",
                    directed=True,
                    collapsible=True,
                    link={'labelProperty': 'label', 'renderLabel': True}
                    )
>>>>>>> 6f6a9624da414e66674de21213f6c8f387db8519
    if algo_type == "Shortest Path":
      if chosen_person_a != "" and chosen_person_b != "" and chosen_person_a != chosen_person_b:
        analysis_results = algos.shortest_path(chosen_person_a, chosen_person_b)
        sp_store = TripleStore()
        if len(analysis_results) > 0:
          for idx, connection in enumerate(analysis_results):
            n1 = connection.replace(" ", "_")
            if idx + 1 < len(analysis_results):
              n2 = analysis_results[idx + 1]
              sp_store.add_triple(connection, "knows", n2, "")
            sp_store, _ = load_persons(n1, sp_store)
          agraph(list(sp_store.getNodes()), (sp_store.getEdges()), config)
        else:
          st.write("None connections found. Try something else.")
      else:
        st.write("Choose choose different persons first.")
    else:
      agraph(list(store.getNodes()), (store.getEdges()), config)

