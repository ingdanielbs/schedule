import pandas as pd
import json

from ingreso.login import connect

def count_instructors():
    df = pd.read_excel('static/datalog/datos.xls')   
    df = df[df['role'].isin(['INSTRUCTOR', 'INSTRUCTOR_APOYO'])]
    df = df['role'].count()
    return df

def count_not_approved_rap():      
    with open('static/competencias.json', 'r', encoding='utf-8') as archivo_json:
        competencias = json.load(archivo_json)        
        not_approved = [item for item in competencias if item['juicio'] == 'NO APROBADO' and item['estado'] in ['EN FORMACION', 'CONDICIONADO'] ]        
    return not_approved 

def count_courses():    
    with open('static/horarios/1-2024.json', 'r', encoding='utf-8') as archivo_json:
        competencias = json.load(archivo_json)        
        fichas = []
        for item in competencias:
            fichas.append(item['FICHA'])
        fichas = list(set(fichas))        
        return len(fichas)
    
def count_instructors_contract():
    client = connect()
    if client:
        db = client["sara"]
        collection = db["users"]        
        users = collection.find()        
        data = list(users)
        df = pd.DataFrame(data)
        df = df[df['contract_type'].isin(['PLANTA', 'CONTRATISTA'])]        
        df = df[df['role'].isin(['INSTRUCTOR', 'INSTRUCTOR_APOYO'])]
        df = df['contract_type'].value_counts()
        return df.to_dict() if len(df) > 0 else None
    return None

def count_students_status():
    with open('static/competencias.json', 'r', encoding='utf-8') as archivo_json:
        data = json.load(archivo_json)
        data = pd.DataFrame(data)
        data = data['estado'].value_counts()
        return data.to_dict() if len(data) > 0 else None
    return None
        
        




        
    