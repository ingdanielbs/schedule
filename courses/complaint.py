import pandas as pd
import json
def complaints_students():        
    url = 'https://docs.google.com/spreadsheets/u/1/d/1NtboerXUyYT8kRm2tkJdrWq8Tn8GDBMFhh2PvfkB_oU/export?format=csv'
    df = pd.read_csv(url)    
    df['Evidencias'] = df['En este espacio se deberán montar las evidencias de los refuerzos pedagógicos aplicados al aprendiz o cualquier soporte que justifique la citación al comité. (solo archivos PDF)'].apply(lambda x: json.loads(x)[0]['link'] if x else None)   
   
    df.columns = ['id', 'fecha', 'hora_finalizacion', 'correo', 'nombre', 'nombre_completo_instructor', 'numero_documento_identidad', 'nombre_programa', 'ficha', 'nombre_completo_aprendiz', 'tipo_documento', 'documento', 'correo_electronico2', 'motivo', 'descripcion_motivo', 'evidencias', 'competencia', 'resultados_aprendizaje', 'powerapps_id', 'link_evidencias']
      
    df['fecha'] = pd.to_datetime(df['fecha'], format='%m/%d/%Y %I:%M:%S %p')
    
    df = df.sort_values(by=['fecha'], ascending=False)           
    
    df = df.drop(columns=['id', 'correo_electronico2', 'evidencias', 'competencia', 'resultados_aprendizaje', 'powerapps_id'])
    df = df.to_dict('records')
    return df


def committe_history(document):
    df = pd.read_excel('static/committee_history/comites.xlsx')

    df.columns = ['PROGRAMA', 'FICHA', 'INSTRUCTOR_REPORTA', 'NOMBRE_INSTRUCTOR', 'NOMBRE_APRENDIZ', 'DOCUMENTO', 'QUEJA', 'MOTIVO', 'ASISTENCIA', 'DECISION', 'FECHA']
    #quitar la hora de la FECHA DEL COMITÉ
    df['FECHA'] = df['FECHA'].dt.date

    #Filtrar por el documento del aprendiz
    df = df[df['DOCUMENTO'] == document]
    
    df = df.to_dict('records')
    return df

