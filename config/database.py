from pymongo import MongoClient
from dotenv import load_dotenv
import os
envPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.dirname(envPath)
dotenvPath = os.path.join(rootPath, '.env')
load_dotenv(dotenvPath)
mongoUrl = os.getenv("MONGO_URL")
client = MongoClient(mongoUrl)
db = client.foomonkeys123
discountsTable = db["Discounts"]
