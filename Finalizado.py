#!/usr/bin/env python3

import requests
import os
import json
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import random
from datetime import datetime, timedelta

def obtener_datos_covid_por_fecha(fecha):
    url = f"https://api.covidtracking.com/v1/us/{fecha}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            # Aquí puedes procesar los datos como desees
            print(f"Fecha: {datos['date']}")
            print(f"Casos confirmados: {datos['positive']}")
            print(f"Fallecimientos: {datos['death']}")

            # Definir la ruta de la carpeta "old"
            carpeta_old = "old"
            # Verificar si la carpeta "old" existe, si no, crearla
            if not os.path.exists(carpeta_old):
                os.makedirs(carpeta_old)

            # Actualizar la ruta del archivo para que esté dentro de la carpeta "old"
            nombre_archivo = os.path.join(carpeta_old, f"datos_covid_{fecha}.json")
            with open(nombre_archivo, "w") as archivo:
                json.dump(datos, archivo, indent=4)
                print(f"Archivo JSON guardado en: {os.path.abspath(nombre_archivo)}")
        else:
            print(f"Error al obtener datos (código de estado {response.status_code})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fecha_deseada = "20200501"  # Cambia la fecha según tus necesidades
    obtener_datos_covid_por_fecha(fecha_deseada)



def generar_datos_json_ciudades_paises():
    # Generar datos de ejemplo para ciudades y países
    datos_ciudades = [
        {"id": 1, "ID_ciudad": 1, "nombre_ciudad": "madrid", "coordenadas": "40.4168° N, 3.7038° W"},
        {"id": 2, "ID_ciudad": 2, "nombre_ciudad": "paris", "coordenadas": "41.3851° N, 2.1734° E"},
        {"id": 3, "ID_ciudad": 3, "nombre_ciudad": "roma", "coordenadas": "39.4699° N, 0.3763° W"},
        {"id": 4, "ID_ciudad": 4, "nombre_ciudad": "pekin", "coordenadas": "37.3886° N, 5.9821° W"},
        {"id": 5, "ID_ciudad": 5, "nombre_ciudad": "lima", "coordenadas": "43.2630° N, 2.9346° W"},
        {"id": 6, "ID_ciudad": 6, "nombre_ciudad": "melburne", "coordenadas": "41.6488° N, 0.8891° W"}
    ]

    datos_paises = [
        {"id": 1, "id_pais": 1, "nombre_pais": "España"},
        {"id": 2, "id_pais": 2, "nombre_pais": "Francia"},
        {"id": 3, "id_pais": 3, "nombre_pais": "Italia"},
        {"id": 4, "id_pais": 4, "nombre_pais": "China"},
        {"id": 5, "id_pais": 5, "nombre_pais": "Peru"},
        {"id": 6, "id_pais": 6, "nombre_pais": "Australia"}
    ]

    # Guardar datos de ciudades en JSON
    with open("ciudades.json", "w") as outfile:
        json.dump(datos_ciudades, outfile, indent=4)

    # Guardar datos de países en JSON
    with open("paises.json", "w") as outfile:
        json.dump(datos_paises, outfile, indent=4)

    print("Archivos JSON de ciudades y países generados exitosamente.")

# Invocar la función para generar los archivos JSON
generar_datos_json_ciudades_paises()



def combinar_ciudades_paises_en_json(archivo_ciudades, archivo_paises, archivo_salida):
    # Leer el archivo JSON de ciudades
    with open(archivo_ciudades, "r") as file_ciudades:
        datos_ciudades = json.load(file_ciudades)

    # Leer el archivo JSON de países
    with open(archivo_paises, "r") as file_paises:
        datos_paises = json.load(file_paises)

    # Combinar los datos de ciudades y países por el campo "id"
    datos_combinados = {}
    for ciudad in datos_ciudades:
        ciudad_id = ciudad["id"]
        for pais in datos_paises:
            pais_id = pais["id"]
            if ciudad_id == pais_id:
                ciudad.update(pais)
                datos_combinados[ciudad_id] = ciudad
                break

    # Guardar los datos combinados en un nuevo archivo JSON
    with open(archivo_salida, "w") as file_salida:
        json.dump(list(datos_combinados.values()), file_salida, indent=4)

    print("Archivo JSON combinado generado exitosamente.")

# Ejemplo de uso:
combinar_ciudades_paises_en_json("ciudades.json", "paises.json", "ciudades_paises_combinados.json")



def agregar_datos_covid_a_combinado(archivo_combinado, archivo_covid, archivo_salida):
    # Leer el archivo JSON combinado de ciudades y países
    with open(archivo_combinado, "r") as file_combinado:
        datos_combinados = json.load(file_combinado)

    # Leer el archivo JSON de datos COVID
    with open(archivo_covid, "r") as file_covid:
        datos_covid = json.load(file_covid)

    # Agregar los campos de COVID a cada entrada del archivo combinado
    for item in datos_combinados:
        item.update(datos_covid)

    # Guardar el archivo JSON actualizado
    with open(archivo_salida, "w") as file_salida:
        json.dump(datos_combinados, file_salida, indent=4)

    print("Archivo JSON combinado con datos COVID generado exitosamente.")
    
    # Mover el archivo combinado a la carpeta "old"
    shutil.move(archivo_combinado, f"old/{archivo_combinado}")

    print(f"Archivo '{archivo_combinado}' movido a la carpeta 'old'.")

# Ejemplo de uso:
agregar_datos_covid_a_combinado("ciudades_paises_combinados.json", "old/datos_covid_20200501.json", "ciudades_paises_covid_combinados.json")



def quitar_campos(archivo_entrada, archivo_salida):
    # Leer el archivo JSON de entrada
    with open(archivo_entrada, "r") as file_entrada:
        datos = json.load(file_entrada)

    # Eliminar los campos nombre_ciudad, nombre_pais y coordenadas de cada entrada
    for entrada in datos:
        del entrada["nombre_ciudad"]
        del entrada["nombre_pais"]
        del entrada["coordenadas"]

    # Guardar el archivo JSON actualizado
    with open(archivo_salida, "w") as file_salida:
        json.dump(datos, file_salida, indent=4)

    print(f"Los campos 'nombre_ciudad', 'nombre_pais' y 'coordenadas' han sido eliminados del archivo '{archivo_entrada}' y guardados en '{archivo_salida}'.")

    # Mover el archivo de entrada a la carpeta "old"
    shutil.move(archivo_entrada, f"old/{archivo_entrada}")

    print(f"Archivo '{archivo_entrada}' movido a la carpeta 'old'.")    
    
# Ejemplo de uso:
quitar_campos("ciudades_paises_covid_combinados.json", "ciudades_paises_covid_combinados_sin_campos.json")



def convertir_tipo_fecha(datos):
    for item in datos:
        fecha_actual = item.get("date", None)
        if fecha_actual is not None:
            fecha_datetime = datetime.strptime(str(fecha_actual), "%Y%m%d")
            nueva_fecha = fecha_datetime.strftime("%Y-%m-%d")
            item["date"] = nueva_fecha

def replicar_y_modificar_datos(archivo_entrada, archivo_salida):
    # Leer el archivo JSON de entrada
    with open(archivo_entrada, "r") as file_entrada:
        datos_entrada = json.load(file_entrada)

    # Convertir el tipo de datos del campo de fecha
    convertir_tipo_fecha(datos_entrada)

    # Lista para almacenar los datos replicados y modificados
    datos_salida = []

    # Fecha inicial
    fecha_inicial = datetime.strptime("2020-05-01", "%Y-%m-%d")

    # Replicar y modificar cada entrada en base al ID
    for item in datos_entrada:
        id_entrada = item.get("id", None)
        if id_entrada is not None:
            # Reiniciar la fecha a "2020-05-01" cada vez que cambie el ID
            fecha_actual = fecha_inicial

            # Replicar la entrada 120 veces
            for _ in range(120):
                # Crear una copia de la entrada actual
                nueva_entrada = item.copy()

                # Generar un factor multiplicador aleatorio entre 0.5 y 1.5
                factor_multiplicador = round(random.uniform(0.5, 1.5), 2)

                # Aplicar el factor multiplicador a los valores numéricos, excepto al ID
                for key, value in nueva_entrada.items():
                    if isinstance(value, (int, float)) and key not in ["id", "id_pais", "ID_ciudad"]:
                        nueva_entrada[key] = round(value * factor_multiplicador, 2)

                # Actualizar la fecha
                nueva_fecha = fecha_actual.strftime("%Y-%m-%d")
                nueva_entrada["date"] = nueva_fecha

                # Aumentar la fecha en un día
                fecha_actual += timedelta(days=1)

                # Agregar la nueva entrada a la lista de datos de salida
                datos_salida.append(nueva_entrada)

    # Guardar los datos replicados y modificados en un nuevo archivo JSON
    with open(archivo_salida, "w") as file_salida:
        json.dump(datos_salida, file_salida, indent=4)

    print("Archivo JSON replicado y modificado generado exitosamente.")
    
    # Mover el archivo de entrada a la carpeta "old"
    shutil.move(archivo_entrada, f"old/{archivo_entrada}")

    print(f"Archivo '{archivo_entrada}' movido a la carpeta 'old'.")  

# Ejemplo de uso:
replicar_y_modificar_datos("ciudades_paises_covid_combinados_sin_campos.json", "ciudades_paises_covid_replicados_modificados.json")



def contar_entradas_json(archivo):
    # Leer el archivo JSON
    with open(archivo, "r") as file:
        datos = json.load(file)

    # Contar el número de entradas en la lista
    num_entradas = len(datos)

    return num_entradas

# Nombre del archivo JSON creado anteriormente
archivo_json = "ciudades_paises_covid_replicados_modificados.json"

# Llamar a la función para contar las entradas
num_entradas = contar_entradas_json(archivo_json)

print("El archivo JSON contiene", num_entradas, "entradas.")



def agregar_columnas_fecha(archivo_entrada, archivo_salida):
    # Leer el archivo JSON de entrada
    with open(archivo_entrada, "r") as file_entrada:
        datos_entrada = json.load(file_entrada)

    # Agregar columnas de año, mes y día
    for entrada in datos_entrada:
        fecha_actual = entrada.get("date", None)
        if fecha_actual is not None:
            # Obtener el año, mes y día de la fecha
            year, month, day = map(int, fecha_actual.split("-"))
            # Agregar las nuevas columnas al diccionario
            entrada["anyo"] = year
            entrada["mes"] = month
            entrada["dia"] = day

    # Guardar los datos con las nuevas columnas en un nuevo archivo JSON
    with open(archivo_salida, "w") as file_salida:
        json.dump(datos_entrada, file_salida, indent=4)

    print("Se han agregado las columnas de fecha al archivo JSON exitosamente.")
    
    # Mover el archivo de entrada a la carpeta "old"
    shutil.move(archivo_entrada, f"old/{archivo_entrada}")

    print(f"Archivo '{archivo_entrada}' movido a la carpeta 'old'.")  

# Nombre del archivo JSON de entrada y salida
archivo_entrada = "ciudades_paises_covid_replicados_modificados.json"
archivo_salida = "ciudades_paises_covid_con_fecha.json"

# Llamar a la función para agregar las columnas de fecha
agregar_columnas_fecha(archivo_entrada, archivo_salida)



def convertir_json_a_parquet(archivo_json, carpeta_procesado):
    # Leer el archivo JSON
    df = pd.read_json(archivo_json)

    # Convertir el DataFrame a un objeto Table de PyArrow
    table = pa.Table.from_pandas(df)

    # Crear la carpeta "procesado" si no existe
    if not os.path.exists(carpeta_procesado):
        os.makedirs(carpeta_procesado)

    # Nombre del archivo Parquet de salida
    archivo_parquet = os.path.join(carpeta_procesado, "ciudades_paises_covid_con_fecha.parquet")

    # Escribir el objeto Table en un archivo Parquet
    pq.write_table(table, archivo_parquet)

    print("Archivo JSON convertido a Parquet y guardado en la carpeta procesado exitosamente.")

# Nombre del archivo JSON convertido anteriormente
archivo_json = "ciudades_paises_covid_con_fecha.json"

# Carpeta donde se guardará el archivo Parquet
carpeta_procesado = "procesado"

# Llamar a la función para convertir el archivo JSON a Parquet
convertir_json_a_parquet(archivo_json, carpeta_procesado)



def convertir_json_a_parquet(archivo_json, carpeta_procesado):
    # Leer el archivo JSON
    with open(archivo_json, "r") as file_json:
        datos_json = json.load(file_json)

    # Crear un DataFrame de pandas desde los datos JSON
    df = pd.DataFrame(datos_json)

    # Convertir el DataFrame a un objeto Table de PyArrow
    table = pa.Table.from_pandas(df)

    # Crear la carpeta "procesado" si no existe
    if not os.path.exists(carpeta_procesado):
        os.makedirs(carpeta_procesado)

    # Nombre del archivo Parquet de salida
    archivo_parquet = os.path.join(carpeta_procesado, f"{os.path.splitext(os.path.basename(archivo_json))[0]}.parquet")

    # Escribir el objeto Table en un archivo Parquet
    pq.write_table(table, archivo_parquet)

    print(f"Archivo JSON '{archivo_json}' convertido a Parquet y guardado en la carpeta 'procesado' exitosamente: '{archivo_parquet}'.")

# Convertir el archivo de ciudades JSON a Parquet en la carpeta "procesado"
convertir_json_a_parquet("ciudades.json", "procesado")

# Convertir el archivo de países JSON a Parquet en la carpeta "procesado"
convertir_json_a_parquet("paises.json", "procesado")



# Lista de archivos a mover
archivos_a_mover = ["ciudades.json", "ciudades_paises_covid_con_fecha.json", "paises.json"]

# Carpeta de destino
carpeta_old = "old"

# Mover cada archivo a la carpeta "old"
for archivo in archivos_a_mover:
    try:
        shutil.move(archivo, os.path.join(carpeta_old, archivo))
        print(f"Archivo '{archivo}' movido a la carpeta 'old'.")
    except FileNotFoundError:
        print(f"¡Advertencia: el archivo '{archivo}' no se encontró para mover a la carpeta 'old'!")
