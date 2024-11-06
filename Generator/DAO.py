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

def GetAll(table,current,file):
    file.write(f"\n        public IEnumerable<{current}> GetAll()")
    file.write("\n        {")
    file.write(f"\n            SqlConnection conn = DatabaseSingleton.GetInstance();\n")
    file.write(f"\n            using (SqlCommand command = new SqlCommand(SELECT * FROM {current}, conn))")
    file.write("\n            {")
    file.write("\n                SqlDataReader reader = command.ExecuteReader();\n                while (reader.Read())\n                {")
    file.write(f"\n                    {current.capitalize()} {current} = new {current.capitalize()}(")
    for x,i in table.items():
        if(x.capitalize() == current):
            lenght = len(i)
            used = len(i)
            strings = ""
            for z,y in i.items():
                if(y == "int"):
                    strings += f"\n                        Convert.ToInt32(reader[{lenght-used}].ToString()),"
                    used -=1
                else:
                    strings += f"\n                        reader[{lenght-used}].ToString(),"
                    used -=1
            file.write(strings[0:len(strings)-1])
            file.write("\n                    ); ;")
            file.write("\n                    yield return autor;")
            file.write("\n                }")
            file.write("\n                reader.Close();")
            file.write("\n            }")
            file.write("\n        }")


def GenerateDAO(entities):
    tables = GetTables(entities)
    for t in tables:
        file = OpenFile(t)
        json = OpenJson()
        Using(file,json)
        LoadNamespace(file,json) 
        ClassName(t,file)
        GetAll(entities,t,file)
        file.close()