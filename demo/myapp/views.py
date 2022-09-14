from django.shortcuts import render
from django.shortcuts import HttpResponse 
from graphviz import Digraph
import os

eleIdx = 0
nodeIdx = 0
level = 0

class student:
    def __init__(self):
        self.name = ''
        self.element = []
        self.color = ''
lis = []
stack = []

s = Digraph('Query', node_attr={'shape': 'record'}, filename='hello.gv')

def get_node_name(i, str1):
    j = i + 1
    z = 0
    strc = ''
    empty = False
    non_empty = False

    while str1[j] != ':' and str1[j] != '{' and str1[j] != '}':
        strc = strc + str1[j]
        j += 1

    if (strc.find("(") != -1 and strc.find(")") == -1):
        print(strc)
        strc = strc.replace("(", " ")

    strc = strc.replace('"', ' ')
    strc = strc.replace('<', '-')
    strc = strc.replace('>', '-');

    while z < len(strc):
        if strc[z] == '0':
            empty = True
        if strc[z] >= '1' and strc[z] <= '9':
            non_empty = True
        z += 1

    if empty == True and non_empty == False:
        return ''

    if strc.find("false") != -1:
        return ''

    if strc.find("--") != -1:
        return ''

    return strc


def add_node(i, str1):
    global eleIdx
    global nodeIdx
    global lis

    eleIdx = 0
    name = get_node_name(i, str1)
    color = ''

    if name.find("QUERY") != -1:
        color += "red"
    elif name.find("RTE") != -1:
        color += "blue"
    elif name.find("TARGETENTRY") != -1:
        color += "orange"
    elif name.find("RELOPTINFO") != -1:
        color += "green"
    else:
        color += "black"

    lis.append(student())
    nodeIdx = len(lis) - 1
    lis[nodeIdx].name = 'node' + str(nodeIdx)
    lis[nodeIdx].color = color
    lis[nodeIdx].element.append(name)

def graphMain(qstring):
    i = 0
    global eleIdx
    global nodeIdx
    global lis
    global level

    while i < len(qstring):
        if qstring[i] == '{':
            #record last node infos
            if level > 0:
                parentNodeIdx = nodeIdx
                parentEleIdx = eleIdx
                stack.append(nodeIdx)
                stack.append(eleIdx)

            add_node(i, qstring)

            #add link
            if level > 0:
                srcstr = 'node' + str(parentNodeIdx) + ':f' + str(parentEleIdx)
                deststr = 'node' + str(nodeIdx) + ':f' + str(eleIdx)
                s.edge(srcstr, deststr)

            level += 1
            i += 1

        elif qstring[i] == '}':
            if level > 1:
                eleIdx = stack.pop()
                nodeIdx = stack.pop()
            
            level -= 1
            i += 1

        elif qstring[i] == ':':
            name = get_node_name(i, qstring)
            
            if len(name) != 0:
                lis[nodeIdx].element.append(name)
                eleIdx += 1
            
            i += 1

        else:
            i += 1

#final we need add node
def finalAddNode():
    i = 0
    j = 0
    global lis

    while(i < len(lis)):
        nodename = lis[i].name
        colorstyle = lis[i].color
        labelname = ''
        array = lis[i].element
        
        while(j < len(array)):
            if j == len(array) - 1:
                tmp = '<f' + str(j) + '> ' + array[j]
            else:
                tmp = '<f' + str(j) + '> ' + array[j] + '|'

            labelname = labelname + tmp
            j += 1

        s.node(nodename, shape='record', color=colorstyle, label=labelname) 
        i += 1
        j = 0

def reset():
    global eleIdx
    global nodeIdx
    global level
    global lis
    global stack
    global s

    lis.clear()
    stack.clear()
    s.clear()
    s.attr(rankdir='LR', size='100000, 100000')
    
    eleIdx = 0
    nodeIdx = 0
    level = 0

#Create your views here
def index(request):
    if request.method == 'POST':
        qstring = request.POST['query']

        reset()

        graphMain(qstring)
        finalAddNode()
        data = s.source

        return render(request, 'test.html', {'data': data})
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html', {})
