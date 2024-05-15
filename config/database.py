from pymongo import MongoClient
from dotenv import load_dotenv
import os
envPath = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(envPath,'.env'))
mongoUrl = os.getenv("MONGO_URL")
client = MongoClient(mongoUrl)
db = client.foomonkeys123
discountsTable = db["Discounts"]
