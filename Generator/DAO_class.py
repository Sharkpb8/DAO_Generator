import os
import json
import re

def Using(json):
    x = "using System;"
    for i in json["class"]["using"]:
        x += f"\nusing System.{i}"
    x += "\n"
    return x

def Namespace(json):
    x = "namespace "+json["namespace"]
    return x

def ClassName(t):
    x = f"public class {t}"
    return x

def Private(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp =""
            First = True
            for z,y in i.items():
                if First:
                    temp += f"private {y} {z};"
                    First = False
                else:
                    temp += f"\n{indentation}private {y} {z};"
            temp += "\n"
            return temp


def GetSet(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    temp += f"public {y} {z.capitalize()} {{ get => {z}; set => {z} = values; }}"
                    First = False
                else:
                    temp += f"\n{indentation}public {y} {z.capitalize()} {{ get => {z}; set => {z} = values; }}"
            return temp

def Constructor(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = (f"\n{indentation}public {x.capitalize()}(")
            parametrs = ""
            for z,y in i.items():
                parametrs += f"{y} {z}, "
            temp += (parametrs[0:len(parametrs)-2]+")")
            return temp

def properties(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    temp += (f"this.{z} = {z};")
                    First = False
                else:
                    temp += (f"\n{indentation}this.{z} = {z};")
            return temp

def ConstructorWithoutId(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = (f"\n{indentation}public {x.capitalize()}(")
            parametrs = ""
            for z,y in i.items():
                if z.lower() != "id":
                    parametrs += f"{y} {z}, "
            temp += (parametrs[0:len(parametrs)-2]+")")
            return temp
        
def propertiesWithoutId(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    if(z.lower() != "id"):
                        temp += (f"this.{z} = {z};")
                    else:
                        temp += (f"this.{z} = 0;")
                    First = False
                else:
                    if(z.lower() != "id"):
                        temp += (f"\n{indentation}this.{z} = {z};")
                    else:
                        temp += (f"\n{indentation}this.{z} = 0;")
            return temp

def ToString(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ('return $"')
            for z,y in i.items():
                temp += (f"{{{z}}} ")
            temp += ('";')
            return temp

def GetTables(entities):
    tables = []
    for i in entities:
        tables.append(i.capitalize())
    return tables

def OpenFile(table):
    if(os.path.exists("./Output") == False):
        os.mkdir("./Output")
    if(os.path.isfile(f"./Output/{table}.cs")):
        f = open(f"./Output/{table}.cs","w")
        return f
    else:
        f = open(f"./Output/{table}.cs","x")
        return f

def OpenJson():
    j = open('./config.json', 'r')
    config = json.load(j)
    return config

def ReadTemplate():
    f = open(f"./Template/class.txt","r")
    return f

def get_indentation(line):
    match = re.match(r"^\s*", line)
    return match.group(0)

def GenerateClass(entities):
    tables = GetTables(entities)
    for t in tables:
        read = ReadTemplate()
        json = OpenJson()
        file = OpenFile(t)
        for i in read:
            match i:
                case i if "<using>" in i:
                    file.write(i.replace("<using>",Using(json)))
                case i if "<namespace>" in i:
                    file.write(i.replace("<namespace>",Namespace(json)))
                case i if "<class>" in i:
                    file.write(i.replace("<class>",ClassName(t)))
                case i if "<private>" in i:
                    file.write(i.replace("<private>",Private(entities,t,get_indentation(i))))
                case i if "<settergetter>" in i:
                    file.write(i.replace("<settergetter>",GetSet(entities,t,get_indentation(i))))
                case i if "<constructor>" in i:
                    file.write(i.replace("<constructor>",Constructor(entities,t,get_indentation(i))))
                case i if "<properties>" in i:
                    file.write(i.replace("<properties>",properties(entities,t,get_indentation(i))))
                case i if "<constructorwithoutid>" in i:
                    file.write(i.replace("<constructorwithoutid>",ConstructorWithoutId(entities,t,get_indentation(i))))
                case i if "<propertiesWithoutId>" in i:
                    file.write(i.replace("<propertiesWithoutId>",propertiesWithoutId(entities,t,get_indentation(i))))
                case i if "<tostring>" in i:
                    file.write(i.replace("<tostring>",ToString(entities,t,get_indentation(i))))
                case i:
                    file.write(i)
        file.close()
        read.close()
