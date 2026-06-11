import streamlit as st
import pandas as pd
from pyathena import connect
import plotly.express as px
import os
import subprocess
from dotenv import load_dotenv

# Cargar credenciales del .env
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Configuración de página de Streamlit
st.set_page_config(page_title="Cloud Data Lakehouse Dashboard", layout="wide", page_icon="☁️")

st.title("☁️ Serverless Data Lakehouse Analytical Dashboard")
st.markdown("---")

# Función optimizada para conectarse y consultar AWS Athena
@st.cache_data(ttl=60)  # Cachear resultados por 1 minuto
def ejecutar_query_athena(query):
    bucket = str(BUCKET_NAME).strip()
    region = str(AWS_REGION).strip()
    ruta_staging = f"s3://{bucket}/resultados/"
    
    conn = connect(
        aws_access_key_id=AWS_ACCESS_KEY.strip(),
        aws_secret_access_key=AWS_SECRET_KEY.strip(),
        region_name=region,
        s3_staging_dir=ruta_staging,
        work_group="primary",
        schema_name="db_analytics"
    )
    return pd.read_sql(query, conn)

# --- SECCIÓN 1: CONTROL DE INGESTA EN VIVO ---
st.sidebar.header("🕹️ Panel de Control de Ingesta")
st.sidebar.write("Simulá la llegada de un nuevo lote transaccional de producción al Data Lake.")

if st.sidebar.button("🚀 Ejecutar Pipeline ETL (Ingestar 100k registros)"):
    with st.sidebar.spinner("Corriendo pipeline.py y subiendo Parquet a S3..."):
        # Ejecutamos de fondo el script automatizado que creamos antes
        resultado = subprocess.run(["python", "pipeline.py"], capture_output=True, text=True)
        if resultado.returncode == 0:
            st.sidebar.success("¡Pipeline ejecutado con éxito!")
            st.cache_data.clear() # Limpiamos caché para forzar a Athena a leer los nuevos datos
            st.rerun()
        else:
            st.sidebar.error(f"Error en el pipeline: {resultado.stderr}")

# --- SECCIÓN 2: KPIs GLOBALES DE VENTAS POR PAÍS ---
st.header("📊 KPIs Globales de Mercado")

query_kpis = """
SELECT 
    pais, 
    COUNT(*) as transacciones_totales,
    ROUND(SUM(CASE WHEN estado_pago = 'Completado' THEN monto ELSE 0 END), 2) as facturacion_total,
    ROUND(AVG(monto), 2) as ticket_promedio,
    ROUND(COUNT(CASE WHEN estado_pago = 'Fallido' THEN 1 END) * 100.0 / COUNT(*), 2) as porcentaje_fallidas
FROM db_analytics.transacciones_produccion
GROUP BY pais
ORDER BY facturacion_total DESC
"""

try:
    df_kpis = ejecutar_query_athena(query_kpis)
    
    # Mostrar métricas destacadas arriba (Top 1 País por facturación)
    top_pais = df_kpis.iloc[0]['pais']
    top_facturacion = df_kpis.iloc[0]['facturacion_total']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Mercado Líder", top_pais)
    col2.metric("💰 Facturación Máxima Regional", f"USD {top_facturacion:,.2f}")
    col3.metric("📊 Total Registros Auditados", f"{df_kpis['transacciones_totales'].sum():,}")

    st.write("")
    
    # Gráfico de barras interactivo con Plotly
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue Total por País (USD)")
        fig_bar = px.bar(df_kpis, x='pais', y='facturacion_total', text_auto='.2s', color='pais', template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        st.subheader("Tasa de Fallos en Pasarela de Pagos (%)")
        fig_line = px.pie(df_kpis, names='pais', values='porcentaje_fallidas', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

except Exception as e:
    st.error(f"No se pudieron cargar las métricas de Athena: {e}")

# --- SECCIÓN 3: CONTROL DE FRAUDE (MÉTRICAS CRÍTICAS) ---
st.markdown("---")
st.header("🚨 Alertas de Risk Management & Fraude")
st.write("Transacciones aprobadas con montos anómalos o de alto riesgo (> USD 1,400.00)")

query_fraude = """
SELECT id_cliente, pais, producto, monto, fecha
FROM db_analytics.transacciones_produccion
WHERE estado_pago = 'Completado' AND monto > 1400.0
ORDER BY monto DESC
LIMIT 10
"""

try:
    df_fraude = ejecutar_query_athena(query_fraude)
    if not df_fraude.empty:
        st.dataframe(df_fraude, use_container_width=True)
    else:
        st.success("✅ No se detectaron anomalías críticas en el último lote analizado.")
except Exception as e:
    st.error(f"Error al procesar auditoría de riesgo: {e}")


st.markdown("---")
st.subheader("📦 Inteligencia de Producto y Distribución Temporal")

col_prod, col_hora = st.columns(2)

query_productos = """
SELECT 
    producto,
    COUNT(*) as volumen_ventas,
    ROUND(SUM(CASE WHEN estado_pago = 'Completado' THEN monto ELSE 0 END), 2) as revenue_neto,
    ROUND(COUNT(CASE WHEN estado_pago = 'Completado' THEN 1 END) * 100.0 / COUNT(*), 2) as tasa_conversion
FROM db_analytics.transacciones_produccion
GROUP BY producto
ORDER BY revenue_neto DESC
"""

query_horarios = """
SELECT 
    SUBSTRING(fecha, 12, 2) as hora_del_dia,
    COUNT(*) as cantidad_transacciones,
    ROUND(SUM(CASE WHEN estado_pago = 'Completado' THEN monto ELSE 0 END), 2) as facturacion_por_hora
FROM db_analytics.transacciones_produccion
GROUP BY SUBSTRING(fecha, 12, 2)
ORDER BY hora_del_dia ASC
"""

try:
    # Ejecutamos productos
    df_prod = ejecutar_query_athena(query_productos)
    with col_prod:
        st.write("**Revenue y Conversión por Producto**")
        # Gráfico de barras horizontal nativo
        st.bar_chart(data=df_prod, x="producto", y="revenue_neto", color="#31333F")

    # Ejecutamos horarios
    df_hora = ejecutar_query_athena(query_horarios)
    with col_hora:
        st.write("**Picos de Facturación por Hora (Evolución)**")
        # Gráfico de líneas nativo para ver la tendencia de horas
        st.line_chart(data=df_hora, x="hora_del_dia", y="facturacion_por_hora", color="#FF4B4B")

except Exception as e:
    st.error(f"Error al cargar analíticas avanzadas: {e}")