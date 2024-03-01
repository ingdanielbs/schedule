import json
from ingreso.login import connect
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment, PatternFill, Border, Side
from docx import Document

def insert_course(archivo):    
    client = connect()
    df = pd.read_excel(f'static/course-students/{archivo}')
    course_number = int(df.iloc[0, 2].split(' - ')[0])
    program = df.iloc[0, 2].split(' - ')[1]
    status = df.iloc[1, 2]
    if client:
        db = client["sara"]
        collection = db["courses"]
        course = collection.find_one({"course_number": course_number})
        if not course:
            data = {
                "course_number": course_number,
                "program": program,
                "status": status,
            }
            try:
                collection.insert_one(data)
                return True
            except:
                return False         
    return False

def insert_courses_students(archivo):
    client = connect()
    df = pd.read_excel(f'static/course-students/{archivo}')
    course_number = int(df.iloc[0, 2].split(' - ')[0])
    df = df.drop([0, 1, 2, 3])
    df.columns=['document_type', 'document', 'name', 'last_name', 'phone', 'email', 'state']
    df['course_number'] = course_number
    if client:
        db = client["sara"]
        collection = db["courses_students"]
        for index, row in df.iterrows():
            data = {
                "document_type": row['document_type'],
                "document": row['document'],
                "name": row['name'],
                "last_name": row['last_name'],
                "phone": row['phone'],
                "email": row['email'],
                "state": row['state'],
                "course_number": row['course_number']
            }
            try:
                collection.insert_one(data)
            except:
                return False
    return False


def insert_courses_competences():
    client = connect()
    with open('static/competencias.json', 'r', encoding='utf-8') as archivo_json:    
        data = json.load(archivo_json)
        df = pd.DataFrame(data)
        print(df)
        
        if client:
            db = client["sara"]
            collection = db["courses_competences"]            
            collection.delete_many({})            
            
            for index, row in df.iterrows():
                data = {
                    "document_type": row['tipo_documento'],
                    "document": row['numero_documento'],
                    "name": row['nombre'],
                    "last_name": row['apellidos'],
                    "status": row['estado'],
                    "competence": row['competencia'],
                    "rap": row['rap'],
                    "judgment": row['juicio'],
                    "official": row['funcionario'],
                    "course_number": row['ficha'],
                    "program": row['programa']
                }
                collection.insert_one(data)
            return True
    return False

def generate_excel_students(course_number):    
    client = connect()
    if client:
        db = client["sara"]
        collection = db["courses_students"]
        collection_courses = db["courses"]
        students = collection.find({"course_number": course_number})
        course = collection_courses.find_one({"course_number": course_number})
        students = [student for student in students if student['state'] != 'RETIRO VOLUNTARIO' and student['state'] != 'CANCELADO' and student['state'] != 'TRASLADADO']
        students = sorted(students, key=lambda x: x['name'])
        data = []
        for student in students:
            data.append(student)
        df = pd.DataFrame(data)
        df.drop(['_id', 'course_number'],  axis=1, inplace=True)
        df.columns = ['Tipo documento', 'Documento', 'Nombre', 'Apellido', 'Celular', 'Correo', 'Estado']
        df['Nombre completo'] = df['Nombre'] + ' ' + df['Apellido']
        df.drop(['Nombre', 'Apellido'], axis=1, inplace=True)
        df = df[['Tipo documento', 'Documento', 'Nombre completo', 'Celular', 'Correo', 'Estado']]
        workbook = Workbook()
        hoja = workbook.active
        img = Image('static/images/logo-sena.png')
        hoja.add_image(img, f'A1')
        hoja['B2'] = 'Centro de Servicios y Gestión Empresarial'
        hoja['B3'] = 'Coordinación de Teleinformática'
        hoja['A4'] = ''
        hoja['A5'] = 'Ficha:'
        hoja['B5'] = course_number
        hoja['A6'] = 'Programa:'
        hoja['B6'] = course['program']
        hoja['A7'] = ''
        hoja[f'A5'].font = hoja[f'A5'].font.copy(bold=True)
        hoja[f'A6'].font = hoja[f'A6'].font.copy(bold=True)    

        for i in range(2, 4):
            hoja[f'B{i}'].font = hoja[f'C{i}'].font.copy(bold=True)

        hoja['A8'] = 'Tipo documento'
        hoja['B8'] = 'Documento'
        hoja['C8'] = 'Nombre completo'
        hoja['D8'] = 'Celular'
        hoja['E8'] = 'Correo'
        hoja['F8'] = 'Estado'

        rango_celdas = hoja['A8:F8']
        color_fondo = PatternFill(start_color='C5EAE8', end_color='C5EAE8', fill_type='solid')
        for row in rango_celdas:
            for cell in row:
                cell.fill = color_fondo
        hoja.column_dimensions['A'].width = 19
        hoja.column_dimensions['B'].width = 12
        hoja.column_dimensions['C'].width = 35
        hoja.column_dimensions['D'].width = 12
        hoja.column_dimensions['E'].width = 40
        hoja.column_dimensions['F'].width = 14

        for r in dataframe_to_rows(df, index=False, header=False):
            hoja.append(r)       
        
        
        workbook.save(f'static/course-students-excel/{course_number}.xlsx')



def entrega_grupo(course_number):
    # Cargar el documento de plantilla
    doc = Document("Formato_Acta_Entrega_Ficha.docx")

    ficha = course_number
   
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if "[FICHA]" in run.text:
                            run.text = run.text.replace("[FICHA]", ficha)

    # Guardar el documento con la lista insertada
    doc.save(f"Acta_Entrega_Ficha_{ficha}.docx")