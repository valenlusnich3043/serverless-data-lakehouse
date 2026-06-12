import pandas as pd
from faker import Faker
import random
import time
import os
import boto3
from dotenv import load_dotenv

# Cargamos las variables de entorno del archivo .env
load_dotenv()

fake = Faker()

# Configuración de AWS desde el .env
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
BUCKET_NAME = os.getenv("BUCKET_NAME")

def generar_datos(cantidad):
    print(f"📦 1. Generando {cantidad} transacciones en memoria...")
    datos = []
    for _ in range(cantidad):
        datos.append({
            "id_transaccion": fake.uuid4(),
            "fecha": fake.date_time_this_year().isoformat(),
            "id_cliente": random.randint(10000, 99999),
            "producto": random.choice(["Laptop", "Smartphone", "Teclado", "Monitor", "Auriculares"]),
            "monto": round(random.uniform(10.5, 1500.0), 2),
            "pais": random.choice(["Argentina", "Brasil", "Chile", "Uruguay", "Colombia"]),
            "estado_pago": random.choice(["Completado", "Pendiente", "Fallido"])
        })
    return pd.DataFrame(datos)

def transformar_a_parquet(df, path_local):
    print(f"⚡ 2. Optimizando datos a formato Parquet Columnar...")
    df.to_parquet(path_local, engine="pyarrow", compression="snappy")
    peso = os.path.getsize(path_local) / (1024 * 1024)
    print(f"💾 Archivo local optimizado creado ({peso:.2f} MB).")

def subir_a_s3(path_local, nombre_s3):
    print(f"☁️ 3. Conectando con AWS S3 e iniciando subida automatizada...")
    try:
        # Inicializamos el cliente oficial de AWS con nuestras llaves secretas
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        
        # Subimos el archivo al bucket
        s3_client.upload_file(path_local, BUCKET_NAME, nombre_s3)
        print(f"🚀 ¡Éxito! Archivo subido a S3 como: s3://{BUCKET_NAME}/{nombre_s3}")
        return True
    except Exception as e:
        print(f"❌ Error crítico al subir a AWS: {e}")
        return False

if __name__ == "__main__":
    start_total = time.time()
    
    archivo_local = "transacciones.parquet"
    # Guardamos el archivo en la raíz de S3 con un nombre fijo para que Athena lo lea siempre
    nombre_en_s3 = "datos/transacciones_produccion.parquet"

    # Ejecutamos el flujo End-to-End
    df_nuevos_datos = generar_datos(100000)
    transformar_a_parquet(df_nuevos_datos, archivo_local)
    exito = subir_a_s3(archivo_local, nombre_en_s3)
    
    end_total = time.time()
    if exito:
        print(f"\n🎉 [PIPELINE COMPLETADO] Proceso exitoso en {end_total - start_total:.2f} segundos.")