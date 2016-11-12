import string
import collections
import words
import words2
import pickle
import networkx as nx

names = words.dictionary

def binarySearch(nameSearch):
    global names, found, lower_bound, middle_pos, upper_bound

    lower_bound = 0
    upper_bound = len(names)-1
    found = False
    while lower_bound <= upper_bound and not found:
        middle_pos = (lower_bound+upper_bound) // 2
        if names[middle_pos] < nameSearch:
            lower_bound = middle_pos + 1
        elif names[middle_pos] > nameSearch:
            upper_bound = middle_pos - 1
        else:
            found = True
    if found:
        return True
    else:
        return False                         



def constructGraph(dictionary):
    G=nx.Graph()
    G.add_nodes_from(words.dictionary)
    letters=string.ascii_lowercase
    for word in dictionary:
        for i in range(len(word)):
            remove=word[:i]+word[i+1:]
            if binarySearch(remove):
                G.add_edge(word,remove)
            for char in letters:
                change=word[:i]+char+word[i+1:]
                if binarySearch(change) and change!=word:
                    G.add_edge(word,change)
        for i in range(len(word)+1):
            for char in letters:
                add=word[:i]+char+word[i:]
                if binarySearch(add):
                    G.add_edge(word,add)
 
    return G

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

print("First step")
dictionary = words2.dictionary  
graph = constructGraph(dictionary)
print("second step")
nx.write_gpickle(graph,"test2.gpickle")
print("third step")
print(transformWord(graph , 'time' , 'space'))

