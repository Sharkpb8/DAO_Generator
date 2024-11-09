# DAO_Generator

## Overview
This python code can be used to generate DAO and DAO classes for c# applications to reduce the time spent on this repetetive task

## Usage
1. Clone this repository using `git clone https://github.com/Sharkpb8/DAO_Generator.git`
2. Open the folder using any code editor
3. Open `main.py` and create variable that will be dictionary 
4. add your tables and attributes like in the example belowe:
```
entities = {
    "autor":
    {"id":"int","name":"string","last_name":"string","birth_date":"date"},
    "basket":
    {"id":"int","customer_id":"int","book_id":"int","date":"date","ebt":"bit"}
    }
```
5. run the code

## Configuration
There are 2 ways you can configure this code
1. Json configuration
- open `configuration.json`
    -  namespace - set this to the name of your c# project name
    -  Windowed - set this to `true` if you created your application as Windows Forms App otherwise set it to `false`
    -  class and DAO using - in this list add everything that you want to use for example: SqlClient,Xml etc.
example of configurated json:
```
{
    "namespace": "Database_project",
    "Windowed": true,
    "class":{
        "using":["Collections.Generic","Linq","Text","Threading.Tasks"]
    },
    "DAO":{
        "using":["Collections.Generic","Data.SqlClient","Linq","Text","Threading.Tasks","Xml"]
    }
}
```

2. Template configuration
- open folder `Template`
- there are two files `class.txt` and `DAO.txt`
- these are the files that the program uses to create cs files
- there is normal text and than there is text that is enclosed in <>
- notmal text will be inserted into the c# file
- text that is enclosed in <> will be swaped by the generated code
- the generation proces takes place in `Generator/DAO_class.py` or `Generator/DAO.py` in match/case