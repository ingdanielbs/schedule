import pandas as pd
import json

def performance_students(numero_documento):
    with open('static/competencias.json', 'r', encoding='utf-8') as archivo_json:
        data = json.load(archivo_json)
        df = pd.DataFrame(data)
        df = df[df['numero_documento'] == numero_documento]        
        total = df['rap'].value_counts().reset_index()
        approved = df[df['juicio'] == 'APROBADO']
        no_approved = df[df['juicio'] == 'NO APROBADO']
        total_approved = len(approved)
        total_no_approved = len(no_approved)
        percentage_approved = (total_approved / len(total)) * 100
        percentage_no_approved = (total_no_approved / len(total)) * 100
        performance_student = ""
        if percentage_approved >= 99:
            performance_student = "Alto"
        elif percentage_no_approved >= 1:
            performance_student = "Bajo"
        else:
            performance_student = "Bueno"

        performance = {
            "name_student" : df['nombre'].iloc[0] + ' ' + df['apellidos'].iloc[0],
            "status": df['estado'].iloc[0],
            "program": df['programa'].iloc[0],
            "total_approved": total_approved,
            "total_no_approved": total_no_approved,
            "percentage_approved": percentage_approved,
            "percentage_no_approved": percentage_no_approved,
            "performance_student": performance_student,
            "ficha": df['ficha'].iloc[0]
        }
        
        return performance
        


def students_list():
    with open('static/competencias.json', 'r', encoding='utf-8') as archivo_json:
        data = json.load(archivo_json)
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset='numero_documento', keep='first')
        df['nombre_completo'] = df['nombre'] + ' ' + df['apellidos']
        df = df[['numero_documento', 'nombre_completo']]
        df = df.sort_values(by='nombre_completo', ascending=True)
        df = df.reset_index(drop=True)
        df = df.to_dict(orient='records')
        return df