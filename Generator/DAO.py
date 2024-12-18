import os
import json
import re
import shutil

def Using(json):
    temp = "using System;"
    for i in json["DAO"]["using"]:
        temp += f"\nusing System.{i};"
    temp += "\n"
    return temp

def Namespace(json):
    temp = "namespace "+json["namespace"]
    return temp

def ClassName(t):
    temp = f"public class {t}DAO"
    return temp

def GetAll(t,json):
    if json["Windowed"]:
        temp = f"public List<{t.capitalize()}> GetAll()"
    else:
        temp = f"public IEnumerable<{t.capitalize()}> GetAll()"
    return temp

def WinList(t):
    return f"List<{t}> {t.lower()}List = new List<{t}>();"

def Select(t):
    temp = f'using (SqlCommand command = new SqlCommand("SELECT * FROM {t}", conn))'
    return temp

def NewInstance(current):
    temp = (f"{current.capitalize()} {current.lower()} = new {current.capitalize()}")
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
                    elif(y == "DateTime"):
                        temp += f"Convert.ToDateTime(reader[{lenght-used}].ToString()),"
                        used -=1
                    else:
                        temp += f"reader[{lenght-used}].ToString(),"
                        used -=1
                    First = False
                else:
                    if(y == "int"):
                        temp += f"\n{indentation}Convert.ToInt32(reader[{lenght-used}].ToString()),"
                        used -=1
                    elif(y == "DateTime"):
                        temp += f"\n{indentation}Convert.ToDateTime(reader[{lenght-used}].ToString()),"
                        used -=1
                    else:
                        temp += f"\n{indentation}reader[{lenght-used}].ToString(),"
                        used -=1
            return (temp[0:len(temp)-1])
        
def yiel(t,json):
    if json["Windowed"]:
        return f"{t.lower()}List.Add({t.lower()});"
    else:
        return f"yield return {t.lower()};"
    
def WinListReturn(t):
    return f"return {t.lower()}List;"

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
        
def ParamsWithoutid(entities,t,indentation):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            First = True
            for z,y in i.items():
                if First:
                    if z != "id":
                        temp += f'command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z.capitalize()}));'
                        First = False
                else:
                    if z != "id":
                        temp += f'\n{indentation}command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z.capitalize()}));'
            return temp
        
def Delete(t):
    return f"public void Delete(int {t.lower()[0]})"

def DeleteSQL(t):
    return f'using (SqlCommand command = new SqlCommand("DELETE FROM {t} WHERE id = @id", conn))'

def idParam(t):
    return f'command.Parameters.Add(new SqlParameter("@id", {t.lower()[0]}));'

def Update(t):
    return f"public void Update({t} {t.lower()[0]})"

def UpdateSQL(entities,t,json):
    temp = f'using (command = new SqlCommand("update {t} set '
    for x,i in entities.items():
        if(x.capitalize() == t):
            if json["Windowed"]:
                temp += f'{{collum}} = @value " + "where id = @id", conn))'
            else:
                atributes = ""
                for z,y in i.items():
                    if z != "id":
                        atributes += f"{z} = @{z}, "
                temp += atributes[0:len(atributes)-2]+' " + "where id = @id", conn))'
            return temp
        
def Params(entities,t,indentation,json):
    for x,i in entities.items():
        if(x.capitalize() == t):
            temp = ""
            if json["Windowed"]:
                temp += f'command.Parameters.Add(new SqlParameter("@id", id));'
                temp += f'\n{indentation}command.Parameters.Add(new SqlParameter("@value", value));'
            else:
                First = True
                for z,y in i.items():
                    if First:
                        temp += f'command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z.capitalize()}));'
                        First = False
                    else:
                        temp += f'\n{indentation}command.Parameters.Add(new SqlParameter("@{z}", {x.lower()[0]}.{z.capitalize()}));'
            return temp



def GetTables(entities):
    tables = []
    for i in entities:
        tables.append(i.capitalize())
    return tables

def CreateOutput():
    if(os.path.exists("./Output") == False):
        os.mkdir("./Output")

def OpenFile(table,json):
    if(json["Folders"] == "Separate"):
        if(os.path.exists(f"./Output/{table}") == False):
            os.mkdir(f"./Output/{table}")
        if(os.path.isfile(f"./Output/{table}/{table}DAO.cs")):
            f = open(f"./Output/{table}/{table}DAO.cs","w")
            return f
        else:
            f = open(f"./Output/{table}/{table}DAO.cs","x")
            return f
    elif(json["Folders"] == "Combined"):
        if(os.path.exists(f"./Output/DAO") == False):
            os.mkdir(f"./Output/DAO")
        if(os.path.isfile(f"./Output/DAO/{table}DAO.cs")):
            f = open(f"./Output/DAO/{table}DAO.cs","w")
            return f
        else:
            f = open(f"./Output/DAO/{table}DAO.cs","x")
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
    CreateOutput()
    for t in tables:
        read = ReadTemplate()
        json = OpenJson()
        file = OpenFile(t,json)
        for i in read:
            match i:
                case i if "<using>" in i:
                    file.write(i.replace("<using>",Using(json)))
                case i if "<namespace>" in i:
                    file.write(i.replace("<namespace>",Namespace(json)))
                case i if "<class>" in i:
                    file.write(i.replace("<class>",ClassName(t)))
                case i if "<GetAll>" in i:
                    file.write(i.replace("<GetAll>",GetAll(t,json)))
                case i if "<WinList>" in i:
                    if json["Windowed"]:
                        file.write(i.replace("<WinList>",WinList(t)))
                case i if "<select>" in i:
                    file.write(i.replace("<select>",Select(t)))
                case i if "<NewInstance>" in i:
                    file.write(i.replace("<NewInstance>",NewInstance(t)))
                case i if "<Reader>" in i:
                    file.write(i.replace("<Reader>",Reader(entities,t,get_indentation(i))))
                case i if "<yield>" in i:
                    file.write(i.replace("<yield>",yiel(t,json)))
                case i if "<WinListReturn>" in i:
                    if json["Windowed"]:
                        file.write(i.replace("<WinListReturn>",WinListReturn(t)))
                case i if "<Save>" in i:
                    file.write(i.replace("<Save>",Save(t)))
                case i if "<InseretSQL>" in i:
                    file.write(i.replace("<InseretSQL>",InseretSQL(entities,t)))
                case i if "<ParamsWithoutid>" in i:
                    file.write(i.replace("<ParamsWithoutid>",ParamsWithoutid(entities,t,get_indentation(i))))
                case i if "<Delete>" in i:
                    file.write(i.replace("<Delete>",Delete(t)))
                case i if "<DeleteSQL>" in i:
                    file.write(i.replace("<DeleteSQL>",DeleteSQL(t)))
                case i if "<idParam>" in i:
                    file.write(i.replace("<idParam>",idParam(t)))
                case i if "<Update>" in i:
                    file.write(i.replace("<Update>",Update(t)))
                case i if "<UpdateSQL>" in i:
                    file.write(i.replace("<UpdateSQL>",UpdateSQL(entities,t,json)))
                case i if "<Params>" in i:
                    file.write(i.replace("<Params>",Params(entities,t,get_indentation(i),json)))
                case i:
                    file.write(i)
        file.close()
        read.close()