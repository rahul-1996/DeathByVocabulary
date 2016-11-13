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

G=nx.read_gpickle('test3.gpickle')

def generateStartEnd():
    flag = True
    while flag:
        node1=random.choice(G.nodes())
        node2 = random.choice(G.nodes())
        try:
            isConnected=nx.bidirectional_dijkstra(G,node1,node2)
        except:
            node1=random.choice(G.nodes())
            node2=random.choice(G.nodes())
        words=transformWord(G,node1,node2)
        if len(words) > 3 and len(words) < 8:
            flag=False
    return words

def generateOptions(words):
    options=[]
    for i in words:
        randChoice = random.choice(G.neighbors(i))
        if randChoice not in words:
            options.append(randChoice)
    return options

@app.route('/')
def gg():
    words = generateStartEnd()
    options = generateOptions(words)
    return render_template('index.html',words=map(json.dumps,words),options=map(json.dumps,options))