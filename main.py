def Private(table):
    for x,i in table.items():
        if(x == t):
            for z,y in i.items():
                print("        private",y,z+";")
            print("")

def ClassName():
    print("")
    print("public class",t)
    print("{")
    print("")

def GetSet(table):
    for x,i in table.items():
        if(x == t):
            for z,y in i.items():
                print("        public",y,z.capitalize(),"{"" get =>",z,"; set =>",z,"= values;""}")
            print("")

def Constructor(table):
    for x,i in table.items():
        if(x == t):
            print("        public",x+"(", end=" ")
            for z,y in i.items():
                print(y,z,end =" ")
            print(")")
            print("        {")
            for z,y in i.items():
                print("             this."+z+" = "+z+";")
            print("        }")
            print("")

def ConstructorWithoutId(table):
    for x,i in table.items():
        if(x == t):
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


entities = {
    "autor":
    {"id":"int","name":"string","last_name":"string","birth_date":"date"},
    "basket":
    {"id":"int","customer_id":"int","book_id":"int","date":"date","ebt":"bit"}
    }

tables = []
for i in entities:
    tables.append(i)

for t in tables:
    ClassName()
    Private(entities)
    GetSet(entities)
    Constructor(entities)   
    ConstructorWithoutId(entities)
