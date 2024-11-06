import os
import json

def OpenFile(table):
    if(os.path.exists("./Output") == False):
        os.mkdir("./Output")
    if(os.path.isfile(f"./Output/{table}DAO.cs")):
        f = open(f"./Output/{table}DAO.cs","w")
        return f
    else:
        f = open(f"./Output/{table}DAO.cs","x")
        return f

def OpenJson():
    j = open('./config.json', 'r')
    config = json.load(j)
    return config

def GetTables(entities):
    tables = []
    for i in entities:
        tables.append(i.capitalize())
    return tables

def Using(file,json):
    file.write("using System;")
    for i in json["DAO"]["using"]:
        file.write(f"\nusing System.{i}")
    file.write("\n")

def LoadNamespace(file,json):
    file.write("\nnamespace "+json["namespace"])
    file.write("{")

def ClassName(current,file):
    file.write(f"\n    public class {current}\n")
    file.write("    {\n")

def GetAll(entities,table,file):
    file.write(f"public IEnumerable<{table}> GetAll()")
    file.write(f"")

def GenerateDAO(entities):
    tables = GetTables(entities)
    for t in tables:
        file = OpenFile(t)
        json = OpenJson()
        Using(file,json)
        LoadNamespace(file,json) 
        ClassName(t,file)
        file.close()