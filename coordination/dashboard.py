import pandas as pd
import json

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
        
    