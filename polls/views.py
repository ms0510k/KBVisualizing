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

def ontologyDemo(request):
    return render(request, "../templates/ontologyDemo.html")

g = rdflib.Graph()

def readData(input_file):
    global l_org, l
    i = 0
    for line in input_file:
        print(line)
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

        # def get_path(wildcard):
        #     app = wx.App(None)
        #     style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        #     dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
        #     if dialog.ShowModal() == wx.ID_OK:
        #         path = dialog.GetPath()
        #     else:
        #         path = None
        #     dialog.Destroy()
        #     return path
        #
        # filePath = get_path('*.owl;*.nt')
        #
        # if filePath == None:
        #     content = False

        if content:
            filePath = os.path.join(BASE_DIR, "polls/static/data/test_data.nt")

            if '.nt' in filePath:
                input_file = open(filePath, 'r')
                readData(input_file)
                if len(l_org) > 200:
                    ntDraw(random.sample(l_org, 200))
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
                            print(s.split('#'))
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
                    print(n)
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

def depth(request):  ##### depth select #####
    if request.method == 'POST':
        print("depth")


        return HttpResponse("depth", content_type='text/html')

def targetProperty(request):  ##### targetProperty select #####
    global l_org, l, targetPropertyTriples, targetPropertyTriplesRandom
    if request.method == 'POST':
        targetProperty = request.POST.get('targetProperty')
        del targetPropertyTriples[:]
        del targetPropertyTriplesRandom[:]
        print("===============================")
        print(targetPropertyTriples)

        flag = False

        for i in range(len(l_org)):
            if targetProperty == l_org[i][1]:
                print(l_org[i])
                targetPropertyTriples.append(l_org[i])
                flag = True

        # if len(targetPropertyTriples) > 20:
        #     for i in range(20):
        #         print(random.choice(targetPropertyTriples))
        #         targetPropertyTriplesRandom.append(random.choice(targetPropertyTriples))
        #     l = targetPropertyTriplesRandom
        #
        # else:
        #     l = targetPropertyTriples
        l = targetPropertyTriples

        ntDraw(l)
        return HttpResponse(flag, content_type='text/html')

def delTriple(request):  ##### Triple Delete & reDraw #####
    global l_org, l, delSubject, delProperty, delObject
    if request.method == 'POST':
        delSubject = request.POST.get('subject')
        delProperty = request.POST.get('property')
        delObject = request.POST.get('object')
        print(delSubject," / ",delProperty," / ",delObject)
        flag = False

        # print("=========================================")
        # print(l)
        for i in range(len(l)):
            if l[i][0] == delSubject and l[i][2] == delObject:
                print("in ok")
                flag = True
                del l[i]
                break
            else:
                print("no")
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
            print(e1)
            print(r)
            print(e2)
            print(score)
        l.append([lst[0][0].replace(lst[0][0].split('_')[0] + '_', ''), lst[0][1], lst[0][2].replace(lst[0][2].split('_')[0] + '_', '')])
        ntDraw(l)


        return HttpResponse(json.dumps(lst), content_type='application/json')