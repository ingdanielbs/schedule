from pymongo import MongoClient

user = "sara"
password = "sara2024"
conection_string = f"mongodb+srv://{user}:{password}@cluster0.ll5vs9x.mongodb.net/?retryWrites=true&w=majority"

def connect():
    try:
        client = MongoClient(conection_string)       
        return client 
    except Exception as e:        
        return None
    
def register():
    client = connect()
    if client:
        db = client["sara"]
        collection = db["codes"]        
        collection.insert_many([
            {"number": "0000-1"}, 
            {"number": "0000-2"}, 
            {"number": "0000-3"}, 
            {"number": "0000-4"}, 
            {"number": "0000-5"}, 
            {"number": "0000-6"}, 
            {"number": "0000-7"}, 
            {"number": "0000-8"}, 
            

   
           
            ])

register()
