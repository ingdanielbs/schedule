import os
import pandas as pd
import shutil

def rename_files():
    carpeta = 'static/course-competences'
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.xls')]
    try:
        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)
            hoja = pd.read_excel(ruta)
            nombre = hoja.iloc[1, 2]
            nuevo_nombre = os.path.join(carpeta, str(nombre) + '.xls')
            shutil.move(ruta, nuevo_nombre)
        return True
    except:
        return False

def join_files():
    carpeta = 'static/course-competences'
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.xls')]    

    datos_hojas = []

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        xls = pd.ExcelFile(ruta_archivo)
        nombre_hojas = xls.sheet_names
            
        for hoja in nombre_hojas:
            datos_hoja = pd.read_excel(ruta_archivo, sheet_name=hoja)
                
            numero_ficha = datos_hoja.iloc[1, 2]
            programa = datos_hoja.iloc[4, 2]
            datos_hoja = datos_hoja.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            datos_hoja.columns = ['tipo_documento', 'numero_documento', 'nombre', 'apellidos', 'estado', 'competencia', 'rap', 'juicio', 'funcionario']
            datos_hoja['ficha'] = numero_ficha
            datos_hoja['programa'] = programa
                
            datos_hojas.append(datos_hoja)

    datos_completos = pd.concat(datos_hojas)
    datos_completos.to_excel('static/competencias.xlsx', index=False)
    datos_completos.to_json('static/competencias.json', orient='records')