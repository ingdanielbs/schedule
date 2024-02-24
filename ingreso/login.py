import bcrypt
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
        return None

""" def loguear(document):    
    df = pd.read_excel('./static/datalog/datos.xls')
    df = df[df['document'] == int(document)]    
    df = df.to_dict('records') 
    return df[0] if len(df) > 0 else None """

def loguear(document, password):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]      
        user = collection.find_one({"document": document})
        if user:
            if verificar_password(password, user["password"]):                
                return {"name": user["name"], "document": user["document"], "email": user["email"], "phone:": user["phone"], "role": user["role"], "status": user["status"], "gender": user["gender"], "contract_type": user["contract_type"]} 
            else:
                return None
        else:
            return None        
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

def register_user(name, document, email, phone, gender, contract_type, role):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"document": document})
        password = encriptar_password(document[-4:])
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
                "role": role,
                "password": password
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

def instructor_list():
    instructors = get_users()    
    instructors = [instructor for instructor in instructors if instructor["role"] in ["INSTRUCTOR", "INSTRUCTOR_APOYO"] ]     
    instructors = sorted(instructors, key=lambda x: x["name"])
    return instructors

def encriptar_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def verificar_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def change_password_user(document, password, new_password):
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]
        user = collection.find_one({"document": document})
        if user:
            if not verificar_password(password, user["password"]):
                return False
            hashed_password = encriptar_password(new_password)
            collection.update_one({"document": document}, {"$set": {"password": hashed_password}})
            client.close()
            return True
    return False

