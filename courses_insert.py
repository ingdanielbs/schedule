from ingreso.login import connect
import pandas as pd

def insert_course(course_number):
    client = connect()
    df = pd.read_excel(f'{course_number}.xls')
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
            collection.insert_one(data)
            client.close()
            return True
    return False



    
