from django.http import HttpResponse
from django.shortcuts import render
import rdflib
from rdflib import URIRef
import copy
import random
import pandas as pd
import json
import os
from DjangoTest.settings import BASE_DIR

# 모델을 통해 추론된 트리플과 score 데이터 경로
engineDataPath = os.path.join(BASE_DIR, "polls/static/engineData/demo.csv")
data = pd.read_csv(engineDataPath, names=['e1','r','e2','score'])

l_org = []
l = []
delSubject = None
delProperty = None
delObject = None
targetPropertyTriples = []
targetPropertyTriplesRandom = []
targetProperty = None
json_l = []

# 추론 전 트리플 데이터 경
dataPath = 'polls/static/data/demo.nt'
dataCount = 5000

def ontologyDemo(request):
    global l_org, l, delObject, delProperty, delSubject, targetProperty, targetPropertyTriples, targetPropertyTriplesRandom
    l_org = []
    l = []
    delSubject = None
    delProperty = None
    delObject = None
    targetPropertyTriples = []
    targetPropertyTriplesRandom = []
    targetProperty = None
    return render(request, "../templates/ontologyDemo.html")

g = rdflib.Graph()


def readData(input_file):
    global l_org, l
    i = 0
    for line in input_file:
        s, p, o = line.replace('\n', '').replace("concept:", '').replace("concept_", '').split('\t')
        s = s.replace(s.split('_')[0] + '_', '')
        o = o.replace(o.split('_')[0] + '_', '')
        if "latitudelongitude" not in p:
            i += 1
            l_org.append([s, p, o])
            l.append([s, p, o])

def ntDraw(data_l):
    nodes = dict()
    triples = []
    links = dict()
    node_index = 1
    link_index = 1

    for t in data_l:
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

# Data를 읽어오는 함수
def graph(request):
    global l_org, l
    if request.method == 'POST':
        content = True

        if content:
            filePath = os.path.join(BASE_DIR, dataPath)
            if '.nt' in filePath:
                input_file = open(filePath, 'r')
                readData(input_file)
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


def runEngine(request):
    global l_org, l, data, delSubject, delProperty, delObject
    if request.method == 'POST':
        runData = data[data['e1'].str.contains(delSubject) & data['e2'].str.contains(delObject)].sort_values('score', ascending=False)
        lst = []
        for i in range(len(runData)):
            tmp = []
            score = runData.values[i][3]
            e1 = runData.values[i][0]
            r = runData.values[i][1]
            e2 = runData.values[i][2]
            tmp.append(e1)
            tmp.append(r)
            tmp.append(e2)
            tmp.append(score)
            lst.append(tmp)

        l.append([lst[0][0].replace(lst[0][0].split('_')[0] + '_', ''), lst[0][1], lst[0][2].replace(lst[0][2].split('_')[0] + '_', '')])
        ntDraw(l)

        return HttpResponse(json.dumps(lst), content_type='application/json')

# 모델을 통하여 추론된 데이터 전처리
def movieReasoning(request):
    global l_org, l, data, delSubject, delProperty, delObject, json_l
    if request.method == 'POST':
        relation = request.POST.get('relation')
        threshold = request.POST.get('threshold')
        threshold = float(threshold)
        print(type(threshold),threshold)
        runData = data[data['r'].str.contains(relation)].sort_values('score', ascending=False)
        lst = runData.values.tolist()

        def processing(tmp):
            if len(tmp) == 3:
                return [tmp[0].replace(tmp[0].split('_')[0] + '_', ''), tmp[1],
                        tmp[2].replace(tmp[2].split('_')[0] + '_', '')]
            else:
                return [tmp[0].replace(tmp[0].split('_')[0] + '_', ''), tmp[1],
                        tmp[2].replace(tmp[2].split('_')[0] + '_', ''), tmp[3]]

        withScore = []
        for i in range(len(l_org)):
            for j in range(len(lst)):
                if l_org[i][1] in lst[j][1]:
                    if l_org[i][0] in lst[j][0] or l_org[i][2] in lst[j][2]:
                        if processing([lst[j][0], lst[j][1], lst[j][2]]) not in l:
                            withScore.append(processing([lst[j][0], lst[j][1], lst[j][2], round(lst[j][3], 3)]))
                            if lst[j][-1] >= threshold:
                                l.append(processing([lst[j][0], lst[j][1], lst[j][2]]))
                    if l_org[i][2] in lst[j][0] or l_org[i][0] in lst[j][2]:
                        if processing([lst[j][0],lst[j][1],lst[j][2]]) not in l:
                            withScore.append(processing([lst[j][0], lst[j][1], lst[j][2], round(lst[j][3], 3)]))
                            if lst[j][-1] >= threshold:
                                l.append(processing([lst[j][0], lst[j][1], lst[j][2]]))

        ntDraw(l)

        return HttpResponse(json.dumps(withScore), content_type='application/json')

def inferredOnly(request):
    global l_org, l, data, delSubject, delProperty, delObject, json_l
    if request.method == 'POST':
        count = request.POST.get('count')
        if int(count)%2==0:
            ntDraw(l)
        else:
            ntDraw(json_l)

        return HttpResponse(json.dumps(json_l), content_type='application/json')