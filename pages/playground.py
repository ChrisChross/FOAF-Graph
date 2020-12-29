import streamlit as st
from typing import List,Set
from SPARQLWrapper import SPARQLWrapper
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config


def app():
  nodes = []
  edges = []

  nodes.append(Node(id="Spiderman", label="Spid", size=400))
  nodes.append(Node(id="Captain_Marvel", label="marvel", size=400))
  edges.append(Edge(source="Captain_Marvel", target="Spiderman", label="friend_of"))

  # nodes = [Node(id=n['id'], label=n['name']) for n in json_nodes]  # add value to payload
  # edges = [Edge(source=e['sourceId'], target=e['targetId']) for e in json_edges]

  config = Config(width=1600,
                  height=1000,
                  directed=True,
                  nodeHighlightBehavior=True,
                  highlightColor="#F7A7A6",
                  collapsible=True,
                  node={'labelProperty': 'label'},  # config labelProperty
                  link={'labelProperty': 'label', 'renderLabel': True}
  )

  return_value = agraph(nodes=nodes,
                        edges=edges,
                        config=config)

  #agraph(list(store.getNodes()), (store.getEdges()), config)
