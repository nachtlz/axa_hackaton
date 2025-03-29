from app import create_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = create_app()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_NAME")]

app.config["MONGO_DB_CLIENT"] = client
app.config["MONGO_DB"] = db

if __name__ == "__main__":
    app.run(debug=True, port=8050)
