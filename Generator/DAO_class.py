import os

#x is not first capital letter needs fix
def Private(table,current,file):
    for x,i in table.items():
        if(x.capitalize() == current):
            for z,y in i.items():
                file.write("\n        private",y,z+";")

def ClassName(current,file):
    file.write(f"public class {current}\n")
    file.write("{\n")
    file.close()

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

def GenerateClass(entities):
    tables = GetTables(entities)
    for t in tables:
        file = OpenFile(t) 
        ClassName(t,file)
        Private(entities,t,file)
        GetSet(entities,t)
        Constructor(entities,t)     
        ConstructorWithoutId(entities,t)
        ToString(entities,t)
        file.close()
