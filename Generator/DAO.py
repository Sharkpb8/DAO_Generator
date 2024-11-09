import os
import json
import re

def Using(json):
    temp = "using System;"
    for i in json["DAO"]["using"]:
        temp += f"\nusing System.{i}"
    temp += "\n"
    return temp

def Namespace(json):
    temp = "namespace "+json["namespace"]
    return temp

def ClassName(t):
    temp = f"public class {t}"
    return temp

def GetAll(t):
    temp = f"public IEnumerable<{t.capitalize()}> GetAll()"
    return temp

def Select(t):
    temp = f'using (SqlCommand command = new SqlCommand("SELECT * FROM {t}", conn))'
    return temp

def NewInstance(current):
    temp = (f"{current.capitalize()} {current.lower()} = new {current.capitalize()}(")
    return temp

def Reader(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            lenght = len(i)
            used = len(i)
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    if(y == "int"):
                        temp += f"Convert.ToInt32(reader[{lenght-used}].ToString()),"
                        used -=1
                    else:
                        temp += f"reader[{lenght-used}].ToString(),"
                        used -=1
                    First = False
                else:
                    if(y == "int"):
                        temp += f"\n{indentation}Convert.ToInt32(reader[{lenght-used}].ToString()),"
                        used -=1
                    else:
                        temp += f"\n{indentation}reader[{lenght-used}].ToString(),"
                        used -=1
            return (temp[0:len(temp)-1])
        
def yiel(t):
    return f"yield return {t.lower()};"

def Save(t):
    return f"public void Save({t} {t.lower()[0]})"

def InseretSQL(entities,t):
    temp = f'using (command = new SqlCommand("insert into {t} ('
    for x,i in entities.items():
        if(x.capitalize() == t):
            atributes = ""
            for z,y in i.items():
                if z != "id":
                    atributes += f"{z}, "
            temp += atributes[0:len(atributes)-2]+") values ("
            atributes = ""
            for z,y in i.items():
                if z != "id":
                    atributes += f"@{z}, "
            temp += atributes[0:len(atributes)-2]+')", conn))'
            return temp

def Params(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    temp += f'command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z}));'
                    First = False
                else:
                    temp += f'\n{indentation}command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z}));'
            return temp
        
def Delete(t):
    return f"public void Delete(int {t.lower()[0]})"

def DeleteSQL(t):
    return f'using (SqlCommand command = new SqlCommand("DELETE FROM {t} WHERE id = @id", conn))'

def idParam(t):
    return f'command.Parameters.Add(new SqlParameter("@id", {t.lower()[0]}));'



def GetTables(entities):
    tables = []
    for i in entities:
        tables.append(i.capitalize())
    return tables

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

def ReadTemplate():
    f = open(f"./Template/DAO.txt","r")
    return f

def get_indentation(line):
    match = re.match(r"^\s*", line)
    return match.group(0)


def GenerateDAO(entities):
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
                    x = i.replace("<namespace>",Namespace(json))
                    file.write(x)
                case i if "<class>" in i:
                    x = i.replace("<class>",ClassName(t))
                    file.write(x)
                case i if "<GetAll>" in i:
                    x = i.replace("<GetAll>",GetAll(t))
                    file.write(x)
                case i if "<select>" in i:
                    x = i.replace("<select>",Select(t))
                    file.write(x)
                case i if "<NewInstance>" in i:
                    x = i.replace("<NewInstance>",NewInstance(t))
                    file.write(x)
                case i if "<Reader>" in i:
                    x = i.replace("<Reader>",Reader(entities,t,get_indentation(i)))
                    file.write(x)
                case i if "<yield>" in i:
                    x = i.replace("<yield>",yiel(t))
                    file.write(x)
                case i if "<Save>" in i:
                    x = i.replace("<Save>",Save(t))
                    file.write(x)
                case i if "<InseretSQL>" in i:
                    x = i.replace("<InseretSQL>",InseretSQL(entities,t))
                    file.write(x)
                case i if "<Params>" in i:
                    x = i.replace("<Params>",Params(entities,t,get_indentation(i)))
                    file.write(x)
                case i if "<Delete>" in i:
                    x = i.replace("<Delete>",Delete(t))
                    file.write(x)
                case i if "<DeleteSQL>" in i:
                    x = i.replace("<DeleteSQL>",DeleteSQL(t))
                    file.write(x)
                case i if "<idParam>" in i:
                    x = i.replace("<idParam>",idParam(t))
                    file.write(x)
                case i:
                    file.write(i)
        file.close()
        read.close()