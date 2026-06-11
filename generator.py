import pandas as pd
from faker import Faker
import random
import time

# Inicializamos Faker para generar datos aleatorios
fake = Faker()

def generar_datos_transacciones(cantidad_registros):
    print(f"Generando {cantidad_registros} registros ficticios...")
    start_time = time.time()
    
    datos = []
    for _ in range(cantidad_registros):
        datos.append({
            "id_transaccion": fake.uuid4(),
            "fecha": fake.date_time_this_year().isoformat(),
            "id_cliente": random.randint(10000, 99999),
            "producto": random.choice(["Laptop", "Smartphone", "Teclado", "Monitor", "Auriculares"]),
            "monto": round(random.uniform(10.5, 1500.0), 2),
            "pais": fake.country(),
            "estado_pago": random.choice(["Completado", "Pendiente", "Fallido"])
        })
    
    # Convertimos la lista de diccionarios en un DataFrame de Pandas (una estructura de tabla en memoria)
    df = pd.DataFrame(datos)
    
    end_time = time.time()
    print(f"Datos generados en {end_time - start_time:.2f} segundos.")
    return df

if __name__ == "__main__":
    # Generamos 100,000 transacciones
    df_transacciones = generar_datos_transacciones(100000)
    
    # Lo guardamos en formato JSON tradicional
    print("Guardando datos en transacciones.json...")
    df_transacciones.to_json("transacciones.json", orient="records", lines=True)
    print("¡Archivo transacciones.json creado con éxito!")