import pandas as pd

def upl_students(code_course):   
    students_df = pd.read_excel('static/course-students/' + code_course + '.xlsx')
    students_df = students_df.drop([0, 1, 2, 3])   
    students_df.columns = ['documentType', 'documentNumber', 'name', 'lastName', 'cellphone', 'email', 'status']
    students_df['course'] = code_course

    return students_df.to_dict('records')


def upl_competences(code_course):      
    competences_df = pd.read_excel('static/course-competences/' + code_course + '.xlsx')
    competences_df = competences_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    competences_df.columns = ['docType', 'documentNumber', 'name', 'lastname', 'status', 'competence', 'learningResult', 'evaluationJudgment', 'official']    
    competences_df = competences_df.drop(['docType', 'name', 'lastname'], axis=1)
    competences_df['course'] = code_course

    return competences_df.to_dict('records')

    