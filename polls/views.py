from django.http import HttpResponse
from django.shortcuts import render
import rdflib
from rdflib import URIRef
#import wx
import random
import pandas as pd
import json
import os
from DjangoTest.settings import BASE_DIR

engineDataPath = os.path.join(BASE_DIR, "polls/static/engineData/engine_df.csv")
data = pd.read_csv(engineDataPath)

l_org = []
l = []
delSubject = None
delProperty = None
delObject = None
targetPropertyTriples = []
targetPropertyTriplesRandom = []
targetProperty = None
#dataPath = 'polls/static/data/nell-995-simple.nt'
dataPath = 'polls/static/data/test_data.nt'
#dataPath = 'polls/static/data/test.nt'
dataCount = 5000

def ontologyDemo(request):
    return render(request, "../templates/ontologyDemo.html")

g = rdflib.Graph()

def readData(input_file):
    global l_org, l
    i = 0
    for line in input_file:
        #print(line)
        s, p, o = line.replace('\n', '').replace("concept:", '').replace("concept_", '').split('\t')
        s = s.replace(s.split('_')[0] + '_', '')
        o = o.replace(o.split('_')[0] + '_', '')
        if "latitudelongitude" not in p:
            i += 1
            l_org.append([s, p, o])
            l.append([s, p, o])
            # if i <= 200:
            #     l.append([s, p, o])

def ntDraw(data):
    nodes = dict()
    triples = []
    links = dict()
    node_index = 1
    link_index = 1

    for t in data:
        e1, r, e2 = t

        if e1 not in nodes:
            nodes[e1] = node_index
            node_index += 1

        if e2 not in nodes:
            nodes[e2] = node_index
            node_index += 1

        if r not in links:
            links[r] = link_index
            link_index += 1

        triples.append([e1, r, e2])

    myoutput = open(os.path.join(BASE_DIR, "polls/static/data/displayData.json"), 'w')

    myoutput.write('{ "nodes": [')

    i = 0
    for n in nodes:
        myoutput.write('{')
        myoutput.write('"name":"' + n + '",')
        myoutput.write('"label": "",')
        myoutput.write('"id":' + str(nodes[n]))
        myoutput.write('}')
        i += 1
        if i < len(nodes):
            myoutput.write(',')
    myoutput.write('],')

    myoutput.write('"links": [')
    i = 0
    for e1, r, e2 in triples:

        myoutput.write('{')
        source = nodes[e1]
        target = nodes[e2]
        myoutput.write('"source":"' + str(source) + '",')
        myoutput.write('"target": "' + str(target) + '",')
        myoutput.write('"type":' + '"' + r + '"')
        myoutput.write('}')
        i += 1
        if i < len(triples):
            myoutput.write(',')
    myoutput.write(']}')

    myoutput.close()

def graph(request):  ##### graph #####
    global l_org, l
    if request.method == 'POST':
        content = True

        if content:
            filePath = os.path.join(BASE_DIR, dataPath)
            if '.nt' in filePath:
                input_file = open(filePath, 'r')
                readData(input_file)
                #ntDraw(l_org)
                if len(l_org) > dataCount:
                    ntDraw(random.sample(l_org, dataCount))
                else:
                    ntDraw(l_org)


            elif '.owl' in filePath:
                g.load(filePath)
                parsed_data = []
                filter_data = ['http://www.w3.org/2002/07/owl#NamedIndividual', 'domain', 'range',
                               'http://www.w3.org/2002/07/owl#Class', 'http://www.w3.org/2002/07/owl#Ontology',
                               'http://www.w3.org/2002/07/owl#ObjectProperty']

                for s, p, o in g:
                    x = str(s) + " " + str(p) + " " + str(o)
                    flag = False
                    for z in filter_data:
                        if z in x:
                            flag = True
                    if not flag:
                        if isinstance(s, URIRef) and isinstance(o, URIRef) and "subClassOf" in str(p):
                            parsed_data.append([s.split('#')[-1], p.split('#')[-1], o.split('#')[-1]])

                nodes = dict()
                triples = []
                links = dict()
                node_index = 1
                link_index = 1

                for t in parsed_data:
                    e1, r, e2 = t

                    if e1 not in nodes:
                        nodes[e1] = node_index
                        node_index += 1

                    if e2 not in nodes:
                        nodes[e2] = node_index
                        node_index += 1

                    if r not in links:
                        links[r] = link_index
                        link_index += 1

                    triples.append([e1, r, e2])

                myoutput = open(os.path.join(BASE_DIR, "polls/static/data/displayData.json"), 'w')

                myoutput.write('{ "nodes": [')

                i = 0

                for n in nodes:
                    myoutput.write('{')
                    myoutput.write('"name":"' + n + '",')
                    myoutput.write('"label": "",')
                    myoutput.write('"id":' + str(nodes[n]))
                    myoutput.write('}')
                    i += 1
                    if i < len(nodes):
                        myoutput.write(',')
                myoutput.write('],')

                myoutput.write('"links": [')
                i = 0

                for e1, r, e2 in triples:

                    myoutput.write('{')
                    source = nodes[e1]
                    target = nodes[e2]
                    myoutput.write('"source":"' + str(source) + '",')
                    myoutput.write('"target": "' + str(target) + '",')
                    myoutput.write('"type":' + '"' + r + '"')
                    myoutput.write('}')
                    i += 1
                    if i < len(triples):
                        myoutput.write(',')
                myoutput.write(']}')

                myoutput.close()

        return HttpResponse(content, content_type='text/html')

def exp(request):  ##### exp #####
    if request.method == 'POST':
        print("exp")


        return HttpResponse("exp", content_type='text/html')

def get_depth(depth, kb_df, target_relation):
    # depth 0 : only target relation triples
    prev_df = kb_df[kb_df.p.str.match(target_relation)]
    prev_depth_node = []
    # depth 1 ~~~~
    for i in range(depth):
        depth_node = prev_depth_node + list(prev_df.s.values) + list(prev_df.o.values)
        depth_index = []

        for row, col in kb_df.iterrows():
            if (col['s'] in depth_node or col['o'] in depth_node ) :
                depth_index.append(row)

        # get triples
        depth_df = kb_df.iloc[depth_index]

        #update for next step
        prev_depth_node = depth_node
        prev_df = depth_df

    return prev_df.values.tolist()

def depth(request):  ##### depth select #####
    global l, l_org, targetProperty
    if request.method == 'POST':
        depth = int(request.POST.get('n'))
        data = pd.read_csv(dataPath, sep='\t', names=['s', 'p', 'o'])
        for i in range(len(data)):
            data['s'][i] = data['s'][i].replace(data['s'][i].split('_')[0] + '_', '')
            data['o'][i] = data['o'][i].replace(data['o'][i].split('_')[0] + '_', '')

        l = get_depth(depth, data, targetProperty)
        ntDraw(l)
        result = [depth,len(l)]

        return HttpResponse(json.dumps(result), content_type='application/json')

def targetProperty(request):  ##### targetProperty select #####
    global l_org, l, targetPropertyTriples, targetPropertyTriplesRandom, targetProperty
    if request.method == 'POST':
        targetProperty = request.POST.get('targetProperty')
        del targetPropertyTriples[:]
        del targetPropertyTriplesRandom[:]

        flag = False

        for i in range(len(l_org)):
            if targetProperty == l_org[i][1]:
                targetPropertyTriples.append(l_org[i])
                flag = True

        l = targetPropertyTriples

        ntDraw(l)
        return HttpResponse(flag, content_type='text/html')

def delTriple(request):  ##### Triple Delete & reDraw #####
    global l_org, l, delSubject, delProperty, delObject
    if request.method == 'POST':
        delSubject = request.POST.get('subject')
        delProperty = request.POST.get('property')
        delObject = request.POST.get('object')
        flag = False

        for i in range(len(l)):
            if l[i][0] == delSubject and l[i][2] == delObject:
                flag = True
                del l[i]
                break
        if flag:
            ntDraw(l)
        return HttpResponse(flag, content_type='text/html')

def runEngine(request):  #####  #####
    global l_org, l, data, delSubject, delProperty, delObject
    if request.method == 'POST':
        runData = data[data['e1'].str.contains(delSubject) & data['e2'].str.contains(delObject)].sort_values('score', ascending=False)
        lst = []
        for i in range(len(runData)):
            tmp = []
            score = runData.values[i][-1]
            e1 = runData.values[i][2]
            r = runData.values[i][3]
            e2 = runData.values[i][4]
            tmp.append(e1)
            tmp.append(r)
            tmp.append(e2)
            tmp.append(score)
            lst.append(tmp)

        l.append([lst[0][0].replace(lst[0][0].split('_')[0] + '_', ''), lst[0][1], lst[0][2].replace(lst[0][2].split('_')[0] + '_', '')])
        ntDraw(l)


        return HttpResponse(json.dumps(lst), content_type='application/json')

def objectReasoning(request):  #####  #####
    global l_org, l, data, delSubject, delProperty, delObject
    if request.method == 'POST':
        object = request.POST.get('object')
        threshold = request.POST.get('threshold')
        #print("objectReasoning_test", object)
        #print("threshold_test", threshold)
        ### searching code ###
        test_lst = [object, threshold]


        ### end code ###
        test_nt = [["jim_jackson", "test_p1", "test_o1"],["test_s2", "test_p2", "jim_jackson"],["jim_jackson", "test_p3", "test_o3"]]
        for i in range(len(test_nt)):
            l.append(test_nt[i])

        #print("test//test//test//test//test//test//test//")
        #print(l)
        ntDraw(l)


        return HttpResponse(json.dumps(test_nt), content_type='application/json')