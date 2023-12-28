import os
import pandas as pd

def join_files():
    carpeta = 'static/course-competences'

    # Obtener la lista de archivos XLSX en la carpeta
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.xls')]

        # Crear una lista vacía para almacenar los datos de cada hoja
    datos_hojas = []

        # Iterar sobre cada archivo y leer todas las hojas
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        xls = pd.ExcelFile(ruta_archivo)
        nombre_hojas = xls.sheet_names
            
        # Iterar sobre cada hoja del archivo actual y agregarla a la lista de datos
        for hoja in nombre_hojas:
            datos_hoja = pd.read_excel(ruta_archivo, sheet_name=hoja)
                
            numero_ficha = datos_hoja.iloc[1, 2]
            datos_hoja = datos_hoja.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            datos_hoja.columns = ['tipo_documento', 'nmero_documento', 'nombre', 'apellidos', 'estado', 'competencia', 'rap', 'juicio', 'funcionario']
            datos_hoja['ficha'] = numero_ficha
                
            datos_hojas.append(datos_hoja)

        # Concatenar los datos de todas las hojas en un solo DataFrame
    datos_completos = pd.concat(datos_hojas)
    datos_completos.to_excel('static/competencias.xlsx', index=False)
    datos_completos.to_json('static/competencias.json', orient='records')