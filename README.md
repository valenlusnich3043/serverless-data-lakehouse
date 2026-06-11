# 🏦 End-to-End Serverless Data Lakehouse Dashboard

Este proyecto implementa la arquitectura de un **Data Lakehouse moderno y Serverless** enfocado en el sector FinTech, capaz de procesar, optimizar y analizar grandes volúmenes de transacciones financieras en tiempo real utilizando servicios en la nube de AWS y un frontend interactivo.

## 🚀 Arquitectura del Pipeline
1. **Generación de Datos:** Simulación automatizada de lotes de hasta 100,000 transacciones en formato JSON (datos de clientes, países, montos, pasarelas de pago).
2. **Pipeline ETL & Optimización:** Transformación de datos crudos a formato **Parquet Columnar** con compresión Snappy para reducir costos de almacenamiento y acelerar consultas SQL en más de un 80%.
3. **Storage (AWS S3):** Almacenamiento distribuido y regional de los archivos Parquet procesados.
4. **Motor Serverless Query (AWS Athena):** Catálogo de datos y ejecución de consultas SQL analíticas complejas directamente sobre el Storage de S3.
5. **Capa de Visualización (Streamlit):** Dashboard interactivo que consume las métricas de Athena en tiempo real, aplicando estrategias de caché para optimizar el rendimiento.

## 📊 Dashboard Operativo
<img width="1366" height="631" alt="image" src="https://github.com/user-attachments/assets/c9102344-75bb-425b-b44f-3da633b9e78e" />
<img width="1366" height="301" alt="image" src="https://github.com/user-attachments/assets/d294663b-8cdb-45d9-b7b8-98f147e5b6f8" />
<img width="1366" height="535" alt="image" src="https://github.com/user-attachments/assets/44c52057-db9b-4435-8b4f-35647b1582f2" />
<img width="1366" height="485" alt="image" src="https://github.com/user-attachments/assets/11f10672-017e-4e35-93f1-ef15ea00b741" />


### Key Features Implementadas:
* **Simulación de Ingesta Interactiva:** Botón en frontend que dispara el flujo ETL completo (100k registros por lote).
* **KPIs de Mercado Globales:** Monitoreo analítico de facturación total, tasas de conversión y ticket promedio por región.
* **Risk Management & Auditoría de Fraude:** Sección dedicada a la identificación en tiempo real de transacciones sospechosas de alto monto (> USD 1,400).
* **Inteligencia de Producto:** Análisis de tendencias horarias y distribución de revenue por catálogo de productos.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.14
* **Ecosistema Data:** Pandas, PyArrow (Parquet)
* **Cloud (AWS):** S3 (Simple Storage Service), Athena, IAM
* **Frontend:** Streamlit

## ⚙️ Configuración del Entorno Local

1. Clonar el repositorio.
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Crear un archivo `.env` en la raíz con las credenciales de AWS:
   ```env
   AWS_ACCESS_KEY_ID=tu_access_key
   AWS_SECRET_ACCESS_KEY=tu_secret_key
   AWS_REGION=us-east-2
   BUCKET_NAME=tu-bucket-name

4. Configurar la consola web de Athena con la ruta de staging correspondiente.

5. Ejecutar la aplicación: streamlit run app.py
