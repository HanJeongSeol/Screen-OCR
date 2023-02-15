from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def env_name(name):
    return os.environ.get(name)

try:
    db_client = MongoClient(env_name("MONGODB"))
    mydb = db_client[env_name("DBNAME")]
    collist = mydb.list_collection_names()
    mycol = mydb[env_name("COLLECTION")]
    print("연결성공")
    
except Exception:
    print("연결오류")