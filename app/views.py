from app import app
from flask import render_template
import networkx as nx
import json
import collections
import random


#Citation : transformWord function using BFS adopted from http://www.ardendertat.com/2011/10/17/transform-word/

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
                paths.append(currentPath[:]+[word])
    #no transformation
    return []

G=nx.read_gpickle('test3.gpickle')

def generateStartEnd():
    lower_limit = 3
    upper_limit = 8
    flag = True
    while flag:
        node1=random.choice(G.nodes())
        node2 = random.choice(G.nodes())
        try: # Using networkx function bidrectional_dijkstra
            isConnected=nx.bidirectional_dijkstra(G,node1,node2)
        except:
            node1=random.choice(G.nodes())
            node2=random.choice(G.nodes())
        words=transformWord(G,node1,node2)
        #To make sure edit distance is not too large or too small.
        if len(words) > lower_limit and len(words) < upper_limit:
            flag=False
    return words

def generateOptions(words):
    options=[]
    for i in words:
        randChoice = random.choice(G.neighbors(i))
        if randChoice not in words:
            options.append(randChoice)
    newlist = options + words[1:len(words)-1]
    random.shuffle(newlist)
    return newlist



@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/')
def something() :
    words = generateStartEnd()
    options = generateOptions(words)
    return render_template('index.html',words=words,lengthoptions=len(options),lengthwords=len(words),options=options)
@app.route('/won')
def won():
    return render_template('won.html')
@app.route('/lose')
def lose():
    return render_template('lose.html')    