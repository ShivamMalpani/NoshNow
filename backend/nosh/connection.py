from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("CONNECTION_STRING")
myclient = MongoClient(uri, server_api=ServerApi('1'))
mydb = myclient["NoshNow"]