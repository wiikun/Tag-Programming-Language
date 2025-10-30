import xml.etree.ElementTree as ET

import sys

import ast

if len(sys.argv) != 2:
    print("usage: python tagPL.py file.xml")
    sys.exit(1)

varDict = {}
elseFlag = False

#テーブル定数ここから

def whileHand(elm):
    while bool(int(varView(elm.attrib.get("flag")))):
        funcRun(list(elm))

def iptHand(elm):
    root = ET.parse(elm.text).getroot()
    funcs = root.findall("func")
    funcDict.update(getFuncDict(funcs))
    
def toggleElseFlag():
    global elseFlag
    elseFlag = False if elseFlag else True

TABLE = {
    "print":lambda elm:
        print(varView(elm.text).encode().decode("unicode_escape"),end = elm.attrib.get("end","\n").encode().decode("unicode_escape"))
    ,
    "input":lambda elm:
        varDict.update({elm.attrib.get("name") : input(elm.text or "")})
    ,
    "call":lambda elm:
        funcRun(funcDict[elm.text])
    ,
    "var":lambda elm:
        varDict.update({elm.attrib.get("name") : elm.text})
    ,
    "if":lambda elm:
        (funcRun(elm) if elm.attrib.get("flag") and bool(int(varView(elm.attrib.get("flag")))) else toggleElseFlag())
    ,
    "else":lambda elm:
        (funcRun(elm) and toggleElseFlag if elseFlag else None)
    ,
    "while":whileHand
    ,
    "add":lambda elm:
        varDict.update({elm.attrib.get("var") : varDict[elm.attrib.get("var")] + int(varView(elm.text))})
    ,
    "sub":lambda elm:
        varDict.update({elm.attrib.get("var") : varDict[elm.attrib.get("var")] - int(varView(elm.text))})
    ,
    "mul":lambda elm:
        varDict.update({elm.attrib.get("var") : varDict[elm.attrib.get("var")] * int(varView(elm.text))})
    ,
    "div":lambda elm:
        varDict.update({elm.attrib.get("var") : varDict[elm.attrib.get("var")] / int(varView(elm.text))})
    ,
    "int":lambda elm:
        varDict.update({elm.attrib.get("var") : int(varDict[elm.attrib.get("var")])})
    ,
    "float":lambda elm:
        varDict.update({elm.attrib.get("var") : float(varDict[elm.attrib.get("var")])})
    ,
    "import":iptHand
        
}

#ここまで

def getFuncDict(funcs):
    funcDict = {}
    for func in funcs:
        funcDict[func.attrib.get("name")] = func
    return funcDict
    
def funcRun(func):
    for elm in func:
        if elm.tag != "else":
            elseFlag = False
        TABLE[elm.tag](elm)
        
def varView(name):
    return varDict.get(name[1:],0) if name and name.startswith(".") else fmlEval(name) if name and name.startswith(":") else name

def fmlEval(fml):
    return ast.literal_eval(fml)
    

root = ET.parse(sys.argv[1]).getroot()
funcs = root.findall("func")
funcDict = {}
funcDict.update(getFuncDict(funcs))

funcRun(funcDict["main"])