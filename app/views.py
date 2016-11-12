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

G=nx.read_gpickle('test2.gpickle')

@app.route('/')
def gg():
    node1=random.choice(G.nodes())
    words=G.neighbors(node1)
    while(not G.neighbors(node1) or len(G.neighbors(node1)) < 15):
        node1 = random.choice(G.nodes())
    print(node1)
    check=random.randint(4,8)
    print(check)
    visited=[node1]
    for i in range(check):
        randChoice=random.choice(G.neighbors(node1))
        while((randChoice in visited) or (not G.neighbors(randChoice)) or (len(G.neighbors(randChoice)) < 15)):
            if(len(G.neighbors(randChoice))==1):
                break
            randChoice=random.choice(G.neighbors(node1))
        print(randChoice)
        visited.append(randChoice)
        node1 = randChoice
    print(visited[check])
    words=transformWord(G,visited[0],visited[check])
    return render_template('index.html',words = map(json.dumps,words))