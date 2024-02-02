import pandas as pd
from pymongo import MongoClient

user = "sara"
password = "sara2024"
conection_string = f"mongodb+srv://{user}:{password}@cluster0.ll5vs9x.mongodb.net/?retryWrites=true&w=majority"


def connect():
    try:
        client = MongoClient(conection_string)
        print("Connected to MongoDB")
        return client 
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

""" def loguear(document):    
    df = pd.read_excel('./static/datalog/datos.xls')
    df = df[df['document'] == int(document)]    
    df = df.to_dict('records') 
    return df[0] if len(df) > 0 else None """


def loguear(document):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"document": document})
        client.close()
        return {"name": user["name"], "document": user["document"], "email": user["email"], "phone:": user["phone"], "role": user["role"], "status": user["status"], "gender": user["gender"], "contract_type": user["contract_type"]} 
    return None

