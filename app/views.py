from app import app
from flask import render_template
import networkx as nx
import json
import collections
import random

def transformWord(graph, start, goal):
    paths=collections.deque([ [start] ])
    extended=set()
    while len(paths)!=0:
        currentPath=paths.popleft()
        currentWord=currentPath[-1]
        if currentWord==goal:
            return currentPath
        elif currentWord in extended:
            continue
        extended.add(currentWord)
        transforms=graph[currentWord]
        for word in transforms:
            if word not in currentPath:
                #avoid loops
                paths.append(currentPath[:]+[word])
    #no transformation
    return []

G=nx.read_gpickle('test.gpickle')

@app.route('/')
def gg():
    node1 = random.choice(G.nodes())
    a1 = random.randint(3,7)
    visited = [node1]
    for i in range(a1):       
        lst = G.neighbors(node1)
        rchoice = random.choice(lst)
        while rchoice in visited:
               rchoice = random.choice(lst)
        visited.append(rchoice)
        node1 = rchoice
        
        
    #a1 = random.randint(3,7)
    #for i in range(a1):
    #lst = nx.node_connected_component(G,node1)
    #lst.remove(node1)
    #node2 = random.sample(lst,1)
    
    #while(G.has_edge(node1,node2[0])):
     #   lst = nx.node_connected_component(G,node1)
     #   lst.discard(node1)
     #   node2 = random.sample(lst,1)   

    #length=nx.bidirectional_dijkstra(G,node1,node2)
    #while(length[0]<=1):
    #    node1 = random.choice(G.nodes())
    #    node2 = random.choice(G.nodes())
    #    length=nx.bidirectional_dijkstra(G,node1,node2)

    words = transformWord(G,visited[0],visited[a1])
    
        
    return render_template('index.html',words = map(json.dumps,words),node1 = visited[0],node2 = visited[a1])
