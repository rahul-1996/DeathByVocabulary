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
    flag=True
    while flag:
        node1=random.choice(G.nodes())
        while(not G.neighbors(node1) or len(G.neighbors(node1)) < 20):
            node1 = random.choice(G.nodes())
        print(node1)
        check=random.randint(4,8)
        print(check)
        visited=[node1]
        for i in range(check):
            randChoice=random.choice(G.neighbors(node1))
            while((randChoice in visited) or (not G.neighbors(randChoice)) or (len(G.neighbors(randChoice)) < 20)):
                randChoice=random.choice(G.neighbors(node1))
            print(randChoice)
            visited.append(randChoice)
            node1 = randChoice
        print(visited[check])
        words=transformWord(G,visited[0],visited[check])
        if(len(words) > 4):
            flag = False
    return render_template('index.html',words = map(json.dumps,words))