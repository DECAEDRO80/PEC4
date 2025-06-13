import sys
import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import datetime
import os
from scipy.signal import savgol_filter

def modulo_1():
    print("Carlos Eduardo Romero González")
    #Se inicia con el desarrollo del Ejercicio 1
    # Cargar el archivo CSV en un DataFrame
    df1:pd.DataFrame = pd.read_csv('./media/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250612.csv')

    # 1. Mostrar las 5 primeras filas
    print("Primeras 5 filas:")
    print(df1.head())
    print("\n" + "="*80 + "\n")

    # 2. Mostrar las columnas del dataframe
    print("Columnas del DataFrame:")
    print(df1.columns.tolist())
    print("\n" + "="*80 + "\n")

    # 3. Mostrar la información (info())
    print("Información del DataFrame (info()):")
    print(df1.info())

def modulo_2():
    print("Carlos Eduardo Romero González")
    #Se garantiza que se ejecute la misma lógica del módulo 1
    # Cargar el archivo CSV en un DataFrame
    df1:pd.DataFrame = pd.read_csv('./media/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250612.csv')
    df2:pd.DataFrame = df1
    
    #Se inicia con el desarrollo del Ejercicio 2
    # 1. Renombrar columnas
    nuevos_nombres = {
        'Dia': 'dia',
        'Estació': 'estacio',
        'Nivell absolut (msnm)': 'nivell_msnm',
        'Percentatge volum embassat (%)': 'nivell_perc',
        'Volum embassat (hm3)': 'volum'
    }
    df2 = df2.rename(columns=nuevos_nombres)
    print("DataFrame con columnas renombradas:")
    print(df2.head())
    print("\n" + "="*80 + "\n")

    # 2. Mostrar valores únicos de los nombres de los pantanos
    print("Valores únicos de los pantanos antes de renombrar:")
    print(df2['estacio'].unique())
    print("\n" + "="*80 + "\n")

    # 3. Renombrar los pantanos usando expresiones regulares
    def limpiar_nombre(pantano):
        # Eliminar 'Embassament de ' y todo lo que está entre paréntesis
        return re.sub(r'Embassament de (.*?)\(.*\)', r'\1', pantano).strip()

    df2['estacio'] = df2['estacio'].apply(limpiar_nombre)
    print("Valores únicos de los pantanos después de renombrar:")
    print(df2['estacio'].unique())
    print("\n" + "="*80 + "\n")

    # 4. Crear nuevo dataframe solo con datos de La Baells
    df_baells = df2[df2['estacio'] == 'la Baells']
    print("DataFrame filtrado para La Baells:")
    print(df_baells.head())
    print("\nNúmero de registros para La Baells:", len(df_baells))

def modulo_3():
    print("Carlos Eduardo Romero González")
    #Se garantiza que se ejecute la misma lógica del módulo 1
    # Cargar el archivo CSV en un DataFrame
    df1:pd.DataFrame = pd.read_csv('./media/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250612.csv')
    df2:pd.DataFrame = df1

    #Se garantiza que se ejecute la misma lógica del módulo 2
    nuevos_nombres = {
        'Dia': 'dia',
        'Estació': 'estacio',
        'Nivell absolut (msnm)': 'nivell_msnm',
        'Percentatge volum embassat (%)': 'nivell_perc',
        'Volum embassat (hm3)': 'volum'
    }
    df2 = df2.rename(columns=nuevos_nombres)
    def limpiar_nombre(pantano):
        # Eliminar 'Embassament de ' y todo lo que está entre paréntesis
        return re.sub(r'Embassament de (.*?)\(.*\)', r'\1', pantano).strip()
    df2['estacio'] = df2['estacio'].apply(limpiar_nombre)
    df_baells = df2[df2['estacio'] == 'la Baells']
    
    #Se inicia con el desarrollo del Ejercicio 3
    df_baells3 = pd.DataFrame(columns=df2.columns)
    df_baells3:pd.DataFrame = df_baells

    # 1. Convertir columna 'dia' a datetime
    print("\n" + "="*80 + "\n")
    try:
        df_baells3['dia'] = pd.to_datetime(df_baells3['dia'], dayfirst=True)
    except Exception as e:
        # Captura cualquier otra excepción no prevista
        print(f"Error inesperado: {e}")
    #print(df_baells3)

    # 2. Conteo de los datos
    print(f"Número total de datos: {len(df_baells3)}")
    print("\n" + "="*80 + "\n")

    # 3. Ordenar por día (ascendente)
    df_baells3 = df_baells3.sort_values('dia')
    print("DataFrame ordenado por fecha (ascendente):")
    print(df_baells3[['dia', 'nivell_perc', 'volum']].head())
    print("\n" + "="*80 + "\n")

    # 4. Cuál es la fecha más antigua y cuál es la fecha más reciente
    print(f"Fecha más antigua: {df_baells3['dia'].min()}")
    print(f"Fecha más reciente: {df_baells3['dia'].max()}")
    print("\n" + "="*80 + "\n")

    # 5. Función para convertir fecha a año decimal
    def toYearFraction(dateLocal:datetime):
        def sinceEpoch(dateLocal:datetime):  # returns seconds since epoch
            return (dateLocal - datetime(1970, 1, 1)).total_seconds()
        
        year = dateLocal.year
        startOfThisYear = datetime(year=year, month=1, day=1)
        startOfNextYear = datetime(year=year+1, month=1, day=1)
       
        yearElapsed = sinceEpoch(dateLocal) - sinceEpoch(startOfThisYear)
        yearDuration = sinceEpoch(startOfNextYear) - sinceEpoch(startOfThisYear)
        fraction = yearElapsed / yearDuration
        
        return dateLocal.year + fraction
    
    # 6. Crear columna dia_decimal
    try:
        df_baells3['dia_decimal'] = df_baells3['dia'].apply(lambda x: toYearFraction(x.to_pydatetime()))
    except Exception as e:
        # Captura cualquier otra excepción no prevista
        print(f"Error inesperado: {e}")

    # 7. Visualización
    plt.figure(figsize=(12, 8))
    plt.plot(df_baells3['dia_decimal'], df_baells3['nivell_perc'], label='Porcentaje de volumen', color='blue', linewidth=2)
    plt.title('Carlos Eduardo Romero González', fontsize=14)
    plt.suptitle('Evolución del volumen de agua en La Baells', y=0.93, fontsize=10)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Porcentaje de volumen (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Crear directorio si no existe
    os.makedirs('./img', exist_ok=True)

    # Guardar la imagen
    plt.savefig('./img/labaells_Carlos_Romero.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Gráfico guardado en img/labaells_Carlos_Romero.png")

def modulo_4():
    print("Carlos Eduardo Romero González")
    #Se garantiza que se ejecute la misma lógica del módulo 1
    # Cargar el archivo CSV en un DataFrame
    df1:pd.DataFrame = pd.read_csv('./media/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250612.csv')
    df2:pd.DataFrame = df1

    #Se garantiza que se ejecute la misma lógica del módulo 2
    nuevos_nombres = {
        'Dia': 'dia',
        'Estació': 'estacio',
        'Nivell absolut (msnm)': 'nivell_msnm',
        'Percentatge volum embassat (%)': 'nivell_perc',
        'Volum embassat (hm3)': 'volum'
    }
    df2 = df2.rename(columns=nuevos_nombres)
    def limpiar_nombre(pantano):
        # Eliminar 'Embassament de ' y todo lo que está entre paréntesis
        return re.sub(r'Embassament de (.*?)\(.*\)', r'\1', pantano).strip()
    df2['estacio'] = df2['estacio'].apply(limpiar_nombre)
    df_baells = df2[df2['estacio'] == 'la Baells']
    
    #Se garantiza que se ejecute la misma lógica del módulo 3
    df_baells3 = pd.DataFrame(columns=df2.columns)
    df_baells3:pd.DataFrame = df_baells

    # 1. Convertir columna 'dia' a datetime
    df_baells3['dia'] = pd.to_datetime(df_baells3['dia'], dayfirst=True)

    # 3. Ordenar por día (ascendente)
    df_baells3 = df_baells3.sort_values('dia')

    # 5. Función para convertir fecha a año decimal
    def toYearFraction(dateLocal:datetime):
        def sinceEpoch(dateLocal:datetime):  # returns seconds since epoch
            return (dateLocal - datetime(1970, 1, 1)).total_seconds()
        
        year = dateLocal.year
        startOfThisYear = datetime(year=year, month=1, day=1)
        startOfNextYear = datetime(year=year+1, month=1, day=1)
       
        yearElapsed = sinceEpoch(dateLocal) - sinceEpoch(startOfThisYear)
        yearDuration = sinceEpoch(startOfNextYear) - sinceEpoch(startOfThisYear)
        fraction = yearElapsed / yearDuration
        
        return dateLocal.year + fraction
    
    # 6. Crear columna dia_decimal
    df_baells3['dia_decimal'] = df_baells3['dia'].apply(lambda x: toYearFraction(x.to_pydatetime()))

    # 7. Visualización
    # Extraer los valores de porcentaje de volumen
    y_original = df_baells3['nivell_perc'].values

    # Aplicar el filtro (manejando posibles NaN)
    y_suavizado = savgol_filter(y_original, window_length=1500, polyorder=3, mode='interp')

    # 2. Crear la visualización comparativa
    plt.figure(figsize=(14, 7))

    # Señal original (fina y semitransparente)
    plt.plot(df_baells3['dia_decimal'], y_original, label='Datos originales',color='blue', linewidth=2)

    # Señal suavizada (gruesa y sólida)
    plt.plot(df_baells3['dia_decimal'], y_suavizado, label='Tendencia suavizada', color='orange', linewidth=5)


    plt.title('Carlos Eduardo Romero González', fontsize=14)
    plt.suptitle('Evolución del volumen de agua en La Baells', y=0.93, fontsize=10)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Porcentaje de volumen (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

     # Crear directorio si no existe
    os.makedirs('./img', exist_ok=True)

    # Guardar la imagen
    plt.savefig('./img/labaells_smoothed_Carlos_Romero.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Gráfico guardado en img/labaells_smoothed_Carlos_Romero.png")

def modulo_5():
    print("Carlos Eduardo Romero González")
    #Se garantiza que se ejecute la misma lógica del módulo 1
    # Cargar el archivo CSV en un DataFrame
    df1:pd.DataFrame = pd.read_csv('./media/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250612.csv')
    df2:pd.DataFrame = df1

    #Se garantiza que se ejecute la misma lógica del módulo 2
    nuevos_nombres = {
        'Dia': 'dia',
        'Estació': 'estacio',
        'Nivell absolut (msnm)': 'nivell_msnm',
        'Percentatge volum embassat (%)': 'nivell_perc',
        'Volum embassat (hm3)': 'volum'
    }
    df2 = df2.rename(columns=nuevos_nombres)
    def limpiar_nombre(pantano):
        # Eliminar 'Embassament de ' y todo lo que está entre paréntesis
        return re.sub(r'Embassament de (.*?)\(.*\)', r'\1', pantano).strip()
    df2['estacio'] = df2['estacio'].apply(limpiar_nombre)
    df_baells = df2[df2['estacio'] == 'la Baells']
    
    #Se garantiza que se ejecute la misma lógica del módulo 3
    df_baells3 = pd.DataFrame(columns=df2.columns)
    df_baells3:pd.DataFrame = df_baells

    # 1. Convertir columna 'dia' a datetime
    df_baells3['dia'] = pd.to_datetime(df_baells3['dia'], dayfirst=True)

    # 3. Ordenar por día (ascendente)
    df_baells3 = df_baells3.sort_values('dia')

    # 5. Función para convertir fecha a año decimal
    def toYearFraction(dateLocal:datetime):
        def sinceEpoch(dateLocal:datetime):  # returns seconds since epoch
            return (dateLocal - datetime(1970, 1, 1)).total_seconds()
        
        year = dateLocal.year
        startOfThisYear = datetime(year=year, month=1, day=1)
        startOfNextYear = datetime(year=year+1, month=1, day=1)
       
        yearElapsed = sinceEpoch(dateLocal) - sinceEpoch(startOfThisYear)
        yearDuration = sinceEpoch(startOfNextYear) - sinceEpoch(startOfThisYear)
        fraction = yearElapsed / yearDuration
        
        return dateLocal.year + fraction
    
    # 6. Crear columna dia_decimal
    df_baells3['dia_decimal'] = df_baells3['dia'].apply(lambda x: toYearFraction(x.to_pydatetime()))

    # 7. Visualización
    # Extraer los valores de porcentaje de volumen
    y_original = df_baells3['nivell_perc'].values

    # Aplicar el filtro (manejando posibles NaN)
    y_suavizado = savgol_filter(y_original, window_length=1500, polyorder=3, mode='interp')

    # 2. Crear la visualización comparativa
    plt.figure(figsize=(14, 7))

    # Señal original (fina y semitransparente)
    plt.plot(df_baells3['dia_decimal'], y_original, label='Datos originales',color='blue', linewidth=2)

    # Señal suavizada (gruesa y sólida)
    plt.plot(df_baells3['dia_decimal'], y_suavizado, label='Tendencia suavizada', color='orange', linewidth=5)


    plt.title('Carlos Eduardo Romero González', fontsize=14)
    plt.suptitle('Evolución del volumen de agua en La Baells', y=0.93, fontsize=10)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Porcentaje de volumen (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

    # 3. Identificación visual de periodos de sequía
    # Umbral para considerar sequía (ajustar según necesidades)
    umbral_sequia = 60  # Por ejemplo, bajo 40% de capacidad

    # Resaltar áreas de sequía
    plt.fill_between(df_baells3['dia_decimal'], 
                    y_suavizado, 
                    umbral_sequia, 
                    where=(y_suavizado < umbral_sequia),
                    color='red', 
                    alpha=0.2,
                    label='Posibles periodos de sequía')

    plt.axhline(y=umbral_sequia, color='darkred', linestyle='--', alpha=0.5)

     # Crear directorio si no existe
    os.makedirs('./img', exist_ok=True)

    # Guardar la imagen
    plt.savefig('./img/labaells_smoothed_sequias_Carlos_Romero.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Gráfico guardado en img/labaells_smoothed_Carlos_Romero.png")

def ejecutar_modulo(numero_modulo):
    modulos = {
        1: modulo_1,
        2: modulo_2,
        3: modulo_3,
        4: modulo_4,
        5: modulo_5
    }
    
    if numero_modulo in modulos:
        resultado = modulos[numero_modulo]()
        print(f"El módulo {numero_modulo} devuelve: {resultado}")
    else:
        print(f"Error: El módulo {numero_modulo} no existe. Debe ser un número del 1 al 5.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
         print("Uso: python3 programa.py <número_del_módulo (1-5)>")
         sys.exit(1)
    
    try:
        numero = int(sys.argv[1])
        ejecutar_modulo(numero)
    except ValueError:
        print("Error: El argumento debe ser un número entero entre 1 y 5.")