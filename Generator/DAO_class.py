import os

def Private(table,current):
    for x,i in table.items():
        if(x == current):
            for z,y in i.items():
                print("        private",y,z+";")
            print("")

def ClassName(current):
    print("")
    print("public class",current)
    print("{")
    print("")

def GetSet(table,current):
    for x,i in table.items():
        if(x == current):
            for z,y in i.items():
                print("        public",y,z.capitalize(),"{"" get =>",z,"; set =>",z,"= values;""}")
            print("")

def Constructor(table,current):
    for x,i in table.items():
        if(x == current):
            print("        public",x+"(", end=" ")
            for z,y in i.items():
                print(y,z,end =" ")
            print(")")
            print("        {")
            for z,y in i.items():
                print("             this."+z+" = "+z+";")
            print("        }")
            print("")

def ConstructorWithoutId(table,current):
    for x,i in table.items():
        if(x == current):
            print("        public",x+"(", end=" ")
            for z,y in i.items():
                print(y,z,end =" ")
            print(")")
            print("        {")
            for z,y in i.items():
                if(z != "id"):
                    print("             this."+z+" = "+z+";")
                else:
                    print("             this."+z+" = 0;")
            print("        }")
            print("")

def ToString(table,current):
    print("        public override string ToString()")
    print("        {")
    for x,i in table.items():
        if(x == current):
            print('            return $"', end=" ")
            for z,y in i.items():
                print("{"+z+"}", end=" ")
            print('";')
            print("        }")
            print("}")

def GetTables(entities):
    tables = []
    for i in entities:
        tables.append(i)
    return tables

def CreateFile(table):
    if(os.path.isfile(f"./Output/{table}.cs")):
        return Exception(f"Ve výstupu se nachází nepovolený soubor {table}.cs")
    f = open(f"./Output/{table}.cs","x")
    return f

def GenerateClass(entities):
    tables = GetTables(entities)
    for t in tables:
        file = CreateFile(t)
        Private(entities,t)
        GetSet(entities,t)
        Constructor(entities,t)   
        ConstructorWithoutId(entities,t)
        ToString(entities,t)
