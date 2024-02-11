from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("mongodb+srv://Ananya:Goldenarcs@1@clusternosh.pmbhisy.mongodb.net/?retryWrites=true&w=majority")
myclient = MongoClient(uri, server_api=ServerApi('1'))
mydb = myclient["NoshNow"]