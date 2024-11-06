from Generator.DAO_class import *
from Generator.DAO import *

entities = {
    "autor":
    {"id":"int","name":"string","last_name":"string","birth_date":"date"},
    "basket":
    {"id":"int","customer_id":"int","book_id":"int","date":"date","ebt":"bit"}
    }

GenerateClass(entities)
GenerateDAO(entities)