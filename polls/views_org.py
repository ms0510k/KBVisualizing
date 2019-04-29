from django.http import HttpResponse
from django.shortcuts import render
from DjangoTest.settings import BASE_DIR
import json
import codecs
import socket
import webbrowser
import urllib.request
import pytz

from sklearn.mixture import GaussianMixture

import numpy as np
import math
import csv
import os
import pandas as pd
from datetime import datetime
import rdflib
from rdflib import URIRef
import wx

def ontologyDemo(request):
    return render(request, "../templates/ontologyDemo.html")

g = rdflib.Graph()
def graph(request):  ##### graph #####
    if request.method == 'POST':
        content = True

        #filePath = easygui.fileopenbox(msg=None, title=None, default='*', filetypes=None, multiple=False)

        def get_path(wildcard):
            app = wx.App(None)
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
            dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
            else:
                path = None
            dialog.Destroy()
            return path

        filePath = get_path('*.owl;*.nt')

        if filePath == None:
            content = False

        if content:

            if '.nt' in filePath:
                #g.parse(filePath, format="nt")
                input_file = open(filePath, 'r')
                l = []
                i = 0
                for line in input_file:
                    print(line)
                    s, p, o = line.replace('\n', '').replace("concept:", '').replace("concept_", '').split('\t')
                    if "latitudelongitude" not in p:
                        i += 1
                        if i <= 100:
                            l.append([s, p, o])

                nodes = dict()
                triples = []
                links = dict()
                node_index = 1
                link_index = 1

                for t in l:
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

                myoutput = open('D:\ontology\polls\static\js\list.json', 'w')

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

                myoutput = open('D:\ontology\polls\static\js\list.json', 'w')

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
    if request.method == 'POST':
        print("targetProperty")


        return HttpResponse("targetProperty", content_type='text/html')