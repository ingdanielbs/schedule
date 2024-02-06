import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

user = "sara"
password = "sara2024"
conection_string = f"mongodb+srv://{user}:{password}@cluster0.ll5vs9x.mongodb.net/?retryWrites=true&w=majority"


def connect():
    try:
        client = MongoClient(conection_string)       
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

def get_users():
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        users = collection.find()    
        data = list(users)
        df = pd.DataFrame(data)
        return df.to_dict('records') if len(df) > 0 else None
        
    return None
   
def change_status(document):    
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"document": document})
        if user:            
            status = not user["status"]
            collection.update_one({"document": document}, {"$set": {"status": status}})
            client.close()
            return True
    return False

""" 
name, document, email, phone, gender, contract_type, status, image, role
"""

def register_user(name, document, email, phone, gender, contract_type, role):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"document": document})
        if not user:
            data = {
                "name": name.upper(), 
                "document": document, 
                "email": email, 
                "phone": phone, 
                "gender": gender,
                "contract_type": contract_type,
                "status": True,
                "image": "NULL",
                "role": role
            }
            collection.insert_one(data)
            client.close()
            return True    
    return False

def update_user(id, name, document, email, phone, gender, contract_type, role):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"_id": ObjectId(id)})         
        if user:
            collection.update_one({"_id": ObjectId(id)}, {"$set": {"document":document, "name": name.upper(), "email": email, "phone": phone, 'gender': gender, 'contract_type': contract_type, 'role': role}})
            client.close()
            return True
    return False

def delete_user(id):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"_id": ObjectId(id)})
        if user:
            collection.delete_one({"_id": ObjectId(id)})
            client.close()
            return True
    return False
 

