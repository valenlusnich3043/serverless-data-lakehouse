import pandas as pd
import os
import time

def optimizar_a_parquet():
    archivo_json = "transacciones.json"
    archivo_parquet = "transacciones.parquet"
    
    # 1. Verificar si el JSON existe
    if not os.path.exists(archivo_json):
        print(f"Error: No se encontró el archivo {archivo_json}. Corré primero generator.py")
        return

    print("Leyendo archivo JSON pesado...")
    start_time = time.time()
    
    # 2. Cargar el JSON en un DataFrame de Pandas
    df = pd.read_json(archivo_json, orient="records", lines=True)
    
    # 3. Guardar en formato Parquet comprimido (usando snappy que es el estándar)
    print("Transformando y comprimiendo a formato Parquet...")
    df.to_parquet(archivo_parquet, engine="pyarrow", compression="snappy")
    
    end_time = time.time()
    print(f"¡Optimización completada en {end_time - start_time:.2f} segundos!")
    
    # 4. Comparar tamaños
    peso_json = os.path.getsize(archivo_json) / (1024 * 1024) # Convertir a MB
    peso_parquet = os.path.getsize(archivo_parquet) / (1024 * 1024)
    
    print("\n--- REPORTE DE OPTIMIZACIÓN DE DATOS ---")
    print(f"Peso del archivo JSON original: {peso_json:.2f} MB")
    print(f"Peso del archivo Parquet optimizado: {peso_parquet:.2f} MB")
    print(f"Reducción de espacio: {((peso_json - peso_parquet) / peso_json) * 100:.1f}%")
    print("----------------------------------------")

if __name__ == "__main__":
    optimizar_a_parquet()