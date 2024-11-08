import os
import json

def Private(table,current,file):
    for x,i in table.items():
        if(x.capitalize() == current):
            for z,y in i.items():
                file.write(f"\n        private {y} {z};")
            file.write("\n")

def ClassName(current,file):
    file.write(f"\n    public class {current}\n")
    file.write("    {\n")

def GetSet(table,current,file):
    for x,i in table.items():
        if(x.capitalize() == current):
            for z,y in i.items():
                file.write(f"\n        public {y} {z.capitalize()} {{ get => {z}; set => {z} = values; }}")
            file.write("\n")

def Constructor(table,current,file):
    for x,i in table.items():
        if(x.capitalize() == current):
            file.write(f"\n        public {x.capitalize()}(")
            temp = ""
            for z,y in i.items():
                temp += f"{y} {z}, "
            file.write(temp[0:len(temp)-2])
            file.write(")")
            file.write("\n        {")
            for z,y in i.items():
                file.write(f"\n             this.{z} = {z};")
            file.write("\n        }")
            file.write("\n")

def ConstructorWithoutId(table,current,file):
    for x,i in table.items():
        if(x.capitalize() == current):
            file.write(f"\n        public {x.capitalize()}(")
            temp = ""
            for z,y in i.items():
                temp += f"{y} {z}, "
            file.write(temp[0:len(temp)-2])
            file.write(")")
            file.write("\n        {")
            for z,y in i.items():
                if(z != "id"):
                    file.write(f"\n              this.{z} = {z};")
                else:
                    file.write(f"\n              this.{z} = 0;")
            file.write("\n        }")
            file.write("\n")

def ToString(table,current,file):
    file.write("\n        public override string ToString()")
    file.write("\n        {")
    for x,i in table.items():
        if(x.capitalize() == current):
            file.write('\n            return $"')
            for z,y in i.items():
                file.write(f"{{{z}}} ")
            file.write('";')
            file.write("\n        }")
            file.write("\n    }")
            file.write("\n}")

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

def Namespace(file,json):
    x = "\nnamespace "+json["namespace"]
    x += "{"
    return x

def Using(json):
    x = "using System;"
    for i in json["class"]["using"]:
        x += f"\nusing System.{i}"
    x += "\n"
    return x

def ReadTemplate():
    f = open(f"./Template/class.txt","r")
    return f

def GenerateClass(entities):
    tables = GetTables(entities)
    for t in tables:
        read = ReadTemplate()
        json = OpenJson()
        file = OpenFile(t)
        for i in read:
            match i:
                case i if "<using>" in i:
                    x = i.replace("<using>",Using(json))
                    file.write(x)
                case i if "<namespace>" in i:
                    x = i.replace("<namespace>",Namespace(file,json))
                    file.write(x)
                case i:
                    file.write(i)
        # Using(file,json)
        # LoadNamespace(file,json) 
        # ClassName(t,file)
        # Private(entities,t,file)
        # GetSet(entities,t,file)
        # Constructor(entities,t,file)     
        # ConstructorWithoutId(entities,t,file)
        # ToString(entities,t,file)
        file.close()
        read.close()
