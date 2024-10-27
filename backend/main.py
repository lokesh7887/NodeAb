# from fastapi import FastAPI, Form

# app = FastAPI()

# @app.get('/')
# def read_root():
#     return {'Ping': 'Pong'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     return {'status': 'parsed'}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import networkx as nx

app = FastAPI()

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

# Define data model for incoming pipeline data
class PipelineData(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData):
    try:
        # Extract nodes and edges from the pipeline data
        nodes = pipeline.nodes
        edges = pipeline.edges
        
        # Initialize directed graph
        graph = nx.DiGraph()
        
        # Add nodes to the graph
        for node in nodes:
            graph.add_node(node['id'])
        
        # Add edges to the graph
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])
        
        # Calculate number of nodes and edges
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        
        # Check if the graph is a Directed Acyclic Graph (DAG)
        is_dag = nx.is_directed_acyclic_graph(graph)
        
        # Return the results
        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "is_dag": is_dag
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
