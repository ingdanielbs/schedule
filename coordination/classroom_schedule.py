import pandas as pd

def get_horario_ambiente(numero_ambiente):
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    horas = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
    letras = ['L', 'M', 'MI', 'J', 'V', 'S']

    df = pd.read_excel(f'static/horarios/1-2024.xlsx')
    df = df.drop([0])
    df.columns = ['Source', 'FICHA', 'FORMACION', 'TITULAR', 'TRIMESTRE', 'COMPETENCIA', 'NOMBRE_COMPETENCIA', 'RAP 1', 'RAP 2', 'RAP 3', 'RAP 4', 'RAP 5', 'RAP 6', 'INSTRUCTOR', 'NC2', 'HORAS_SEMANAL', 'NN2', 'h6_7L', 'h7_8L', 'h8_9L', 'h9_10L', 'h10_11L', 'h11_12L', 'h12_13L', 'h13_14L', 'h14_15L', 'h15_16L', 'h16_17L', 'h17_18L', 'h18_19L', 'h19_20L', 'h20_21L', 'h21_22L', 'h6_7M', 'h7_8M', 'h8_9M', 'h9_10M', 'h10_11M', 'h11_12M', 'h12_13M', 'h13_14M', 'h14_15M', 'h15_16M', 'h16_17M', 'h17_18M', 'h18_19M', 'h19_20M', 'h20_21M', 'h21_22M', 'h6_7MI', 'h7_8MI', 'h8_9MI', 'h9_10MI', 'h10_11MI', 'h11_12MI', 'h12_13MI', 'h13_14MI', 'h14_15MI', 'h15_16MI', 'h16_17MI', 'h17_18MI', 'h18_19MI', 'h19_20MI', 'h20_21MI', 'h21_22MI', 'h6_7J', 'h7_8J', 'h8_9J', 'h9_10J', 'h10_11J', 'h11_12J', 'h12_13J', 'h13_14J', 'h14_15J', 'h15_16J', 'h16_17J', 'h17_18J', 'h18_19J', 'h19_20J', 'h20_21J', 'h21_22J', 'h6_7V', 'h7_8V', 'h8_9V', 'h9_10V', 'h10_11V', 'h11_12V', 'h12_13V', 'h13_14V', 'h14_15V', 'h15_16V', 'h16_17V', 'h17_18V', 'h18_19V', 'h19_20V', 'h20_21V', 'h21_22V', 'h6_7S', 'h7_8S', 'h8_9S', 'h9_10S', 'h10_11S', 'h11_12S', 'h12_13S', 'h13_14S', 'h14_15S', 'h15_16S', 'h16_17S', 'h17_18S', 'h18_19S', 'h19_20S', 'h20_21S', 'h21_22S']

    df = df.drop(['Source', 'TITULAR', 'FORMACION', 'COMPETENCIA', 'RAP 1', 'RAP 2', 'RAP 3', 'RAP 4', 'RAP 5', 'RAP 6', 'NC2', 'HORAS_SEMANAL', 'NN2', 'HORAS_SEMANAL',], axis=1)

    # Crear un diccionario para almacenar el horario de cada ambiente
# Crear un diccionario para almacenar el horario de cada ambiente
    horario_ambientes = {}

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        ficha = row['FICHA']
        instructor = row['INSTRUCTOR']

        # Iterar sobre los días
        for dia in dias:
            # Iterar sobre las horas
            for hora in horas:
                # Obtener el valor de la celda correspondiente
                valor = row[f'{hora}{letras[dias.index(dia)]}']

                # Verificar si el valor no es NaN
                if pd.notna(valor):
                    # Crear un diccionario para el ambiente si no existe
                    if valor not in horario_ambientes:
                        horario_ambientes[valor] = {}

                    # Crear un diccionario para el día si no existe
                    if dia not in horario_ambientes[valor]:
                        horario_ambientes[valor][dia] = {}

                    # Crear una lista para la hora si no existe
                    if hora not in horario_ambientes[valor][dia]:
                        horario_ambientes[valor][dia][hora] = []

                    # Agregar la información al diccionario existente
                    horario_ambientes[valor][dia][hora].append({'FICHA': ficha, 'INSTRUCTOR': instructor})

    # Filtrar el diccionario por el ambiente que se desea consultar
    horario_ambiente_deseado = {numero_ambiente: horario_ambientes.get(numero_ambiente, {})}

    for ambiente in horario_ambiente_deseado:        
        for day in dias:
            if day not in horario_ambiente_deseado[ambiente]:
                    horario_ambiente_deseado[ambiente][day] = {}

        for hour in horas:
            if hour not in horario_ambiente_deseado[ambiente][day]:
                horario_ambiente_deseado[ambiente][day][hour] = []

    return horario_ambiente_deseado









    