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
import speech_recognition as sr

#engineDataPath = os.path.join(BASE_DIR, "polls/static/engineData/model_answer.csv")
#engineDataPath = os.path.join(BASE_DIR, "polls/static/engineData/demo.csv")
engineDataPath = os.path.join(BASE_DIR, "polls/static/engineData/wiseKB_answer.csv")

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

#dataPath = 'polls/static/data/display_.nt'
dataPath = 'polls/static/data/display_.nt'
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

def graph(request):  ##### graph #####
    global l_org, l
    if request.method == 'POST':
        kb = request.POST.get('KB')
        content = True

        if content:
            if kb == 'nationality':
                dataPath = 'polls/static/data/display_nation.nt'
            elif kb == 'job':
                dataPath = 'polls/static/data/display_job.nt'
            elif kb == 'employer':
                dataPath = 'polls/static/data/display_emp.nt'
            filePath = os.path.join(BASE_DIR, dataPath)
            print(filePath)
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
        depth = int(request.POST.get('n')) #depth 숫자 받기
        #data = pd.read_csv(dataPath, sep='\t', names=['s', 'p', 'o'])
        data = []
        for line in open(dataPath, 'r'):
            s, p, o = line.replace('\n', '').replace("concept:", '').replace("concept_", '').split('\t')
            data.append([s, p, o])
        data = pd.DataFrame(data)
        data.columns = ['s', 'p', 'o']

        #print(data[0:1])
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

        for i in range(len(l_org)):
            if targetProperty == l_org[i][1]:
                targetPropertyTriples.append(l_org[i])
                flag = True

        l = targetPropertyTriples

        ntDraw(l)
        return HttpResponse(json.dumps(l), content_type='text/html')

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
        #print("=========")
        print(runData)
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

def objectReasoning(request):  ##### nell #####
    global l_org, l, data, delSubject, delProperty, delObject
    if request.method == 'POST':
        object = request.POST.get('object')
        threshold = request.POST.get('threshold')
        threshold = float(threshold)
        print(type(threshold),threshold)
        runData = data[data['e2'].str.contains(object)].sort_values('score', ascending=False)
        lst = []
        json_l = []
        tmp_l = copy.deepcopy(l)
        l = []
        for i in range(len(tmp_l)):
            if tmp_l[i][2] != object:
                l.append(tmp_l[i])
        for i in range(len(runData)):
            tmp = []
            score = runData.values[i][-1]
            e1 = runData.values[i][0]
            r = runData.values[i][1]
            e2 = runData.values[i][2]
            tmp.append(e1)
            tmp.append(r)
            tmp.append(e2)
            tmp.append(score)
            lst.append(tmp)

        # print(lst)
        for i in range(len(lst)):
            if lst[i][3] > threshold:
                l.append([lst[i][0].replace(lst[i][0].split('_')[0] + '_', ''), lst[i][1].replace('concept:', ''),
                          lst[i][2].replace(lst[i][2].split('_')[0] + '_', '')])
                json_l.append([lst[i][0].replace(lst[i][0].split('_')[0] + '_', ''), lst[i][1].replace('concept:', ''),
                               lst[i][2].replace(lst[i][2].split('_')[0] + '_', ''), lst[i][3]])
        print("=======")
        print(len(l))
        print(l)
        ntDraw(l)

        return HttpResponse(json.dumps(json_l), content_type='application/json')

def relationReasoning(request):  ##### nell #####
    global l_org, l, data, delSubject, delProperty, delObject, json_l
    if request.method == 'POST':
        relation = request.POST.get('relation')
        threshold = request.POST.get('threshold')
        threshold = float(threshold)
        print(type(threshold),threshold)
        runData = data[data['r'].str.contains(relation)].sort_values('score', ascending=False)
        lst = []
        result_l = []
        for i in range(len(runData)):
            tmp = []
            score = runData.values[i][-1]
            e1 = runData.values[i][0]
            r = runData.values[i][1]
            e2 = runData.values[i][2]
            tmp.append(e1)
            tmp.append(r)
            tmp.append(e2)
            tmp.append(score)
            lst.append(tmp)

        print('lstlen:',len(lst))
        print(lst)
        #l = []
        print('llen:',len(l))
        for i in range(len(lst)):
            if lst[i][3] > threshold:
                l.append([lst[i][0].replace(lst[i][0].split('_')[0] + '_', ''), lst[i][1].replace('concept:', ''),
                          lst[i][2].replace(lst[i][2].split('_')[0] + '_', '')])
                json_l.append([lst[i][0].replace(lst[i][0].split('_')[0] + '_', ''), lst[i][1].replace('concept:', ''),
                               lst[i][2].replace(lst[i][2].split('_')[0] + '_', '')])
                result_l.append([lst[i][0].replace(lst[i][0].split('_')[0] + '_', ''), lst[i][1].replace('concept:', ''),
                                 lst[i][2].replace(lst[i][2].split('_')[0] + '_', ''), lst[i][3]])
        print("=======")
        print(len(l))
        print(l)
        ntDraw(l)

        return HttpResponse(json.dumps(result_l), content_type='application/json')

def Reasoning(request):  ##### nell #####
    global l_org, l, data, delSubject, delProperty, delObject, json_l
    if request.method == 'POST':
        relation = request.POST.get('relation')
        threshold = request.POST.get('threshold')
        threshold = float(threshold)
        print(type(threshold),threshold)
        runData = data[data['r'].str.contains(relation)].sort_values('score', ascending=False)

        l_df = pd.DataFrame(l)
        l_df.columns = ['e1', 'r', 'e2']
        e1_lst = l_df.e1.values.tolist()
        e2_lst = l_df.e2.values.tolist()
        e = e1_lst + e2_lst
        e = list(set(e))
        reasoningData = runData[(runData.e1.isin(e)) & (runData.score >= threshold)]
        reasoningData_lst = reasoningData.values.tolist()
        reasoningData_lst2 = runData[runData.e1.isin(e)].values.tolist()
        withScore = []
        for i in range(len(reasoningData_lst)):
            if [reasoningData_lst[i][0], reasoningData_lst[i][1], reasoningData_lst[i][2]] not in l:
                l.append([reasoningData_lst[i][0], reasoningData_lst[i][1], reasoningData_lst[i][2]])
        ntDraw(l)
        return HttpResponse(json.dumps(reasoningData_lst2), content_type='application/json')

def movieReasoning_org(request):  ##### nell #####
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
        print('test1')
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
        print('test2')
        ntDraw(l)
        print('test3')
        return HttpResponse(json.dumps(withScore), content_type='application/json')

def inferredOnly(request):  #####  #####
    global l_org, l, data, delSubject, delProperty, delObject, json_l
    if request.method == 'POST':
        count = request.POST.get('count')
        if int(count)%2==0:
            ntDraw(l)
        else:
            ntDraw(json_l)

        return HttpResponse(json.dumps(json_l), content_type='application/json')



def listen():
    print('11')
    r = sr.Recognizer()
    print('22')
    mic = sr.Microphone()
    print('33')
    with mic as source:
        print('44')
        audio = r.listen(source)
    print('55')
    text = r.recognize_google(audio, language = 'ko-KR')
    print('인식한 문장: ',text)
    return text

def speak(x):
    os.system('say '+str(x))

def processing(t, rel):
    subjectDf = data[data.e1.str.contains(t) & data.r.str.contains(rel)]
    df = subjectDf[subjectDf.score == subjectDf.score.max()]
    if rel == 'nationality':
        text = df.e1.values[0] + '의 국적은 ' + df.e2.values[0] + ' 입니다.'
    elif rel == 'employer':
        text = df.e1.values[0] + '의 소속 팀은 ' + df.e2.values[0] + ' 입니다.'
    elif rel == 'job':
        text = df.e1.values[0] + '의 직업은 ' + df.e2.values[0] + ' 입니다.'
    return text

def stt(request):  #####  #####
    global  data
    if request.method == 'POST':
        name = request.POST.get('name')
        rel = request.POST.get('rel')
        print('aaaaaaaaaa')
        #text = listen()
        #print('1')
        text = processing(name, rel)
        #print('2')
        print(text)
        print(rel)
        speak(text)
        return HttpResponse(json.dumps([str(text)]), content_type='application/json')