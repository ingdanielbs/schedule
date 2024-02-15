from ingreso.login import connect
import pandas as pd

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

def insert_courses_competences(archivo):
    client = connect()
    df = pd.read_excel(f'static/course-competences/{archivo}')
    course_number = int(df.iloc[1][2])
    df = df.drop([0,1,2,3,4,5,6,7,8,9,10,11,12])
    df.columns=['document_type', 'document', 'name', 'last_name', 'state', 'competence', 'rap', 'judgment', 'official']
    df['course_number'] = course_number
    if client:
        db = client["sara"]
        collection = db["courses_competences"]
        course = db['courses'].find_one({"course_number": course_number})        
        if course:
            collection.delete_many({"course_number": course_number})
        for index, row in df.iterrows():
            data = {
                "document_type": row['document_type'],
                "document": row['document'],
                "name": row['name'],
                "last_name": row['last_name'],
                "state": row['state'],
                "competence": row['competence'],
                "rap": row['rap'],
                "judgment": row['judgment'],
                "official": row['official'],
                "course_number": row['course_number']
            }
            try:
                collection.insert_one(data)
            except:
                return False
    return False


        