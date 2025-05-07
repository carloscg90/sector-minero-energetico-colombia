
import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt

# Título
st.markdown("<h1 style='text-align: center;'>⚡ Dashboard Sector Minero Energético Colombia. Prueba Carlos Córdoba</h1>", unsafe_allow_html=True)

# Ruta a la base de datos
db_path = "SectorMineroEnergeticoColombia.db"

# Verificar si el archivo existe
if os.path.exists(db_path):
    # Conexión
    conn = sqlite3.connect(db_path)

    # Consulta
    query = "SELECT * FROM eficiencia_energetica"
    data = pd.read_sql_query(query, conn)

    # Mostrar tabla
    st.subheader("📋 Tabla completa: eficiencia_energetica")
    st.dataframe(data)

    # Gráfico de barras de energía generada por proyecto
    st.subheader("📊 Energía generada por proyecto")
    grafico = data.groupby('proyecto_id')['kw_h_generado'].sum()
    st.bar_chart(grafico)

    # Gráfico de barras: promedio de kWh generado por año
    if 'anio' in data.columns:
        st.subheader("📊 Promedio de energía generada por año")
        promedio_anual = data.groupby('anio')['kw_h_generado'].mean()
        st.bar_chart(promedio_anual)

    # Pie chart: distribución total de kWh por tipo de fuente (si existe columna)
    if 'fuente' in data.columns:
        st.subheader("🥧 Distribución por fuente energética")
        pie_data = data.groupby('fuente')['kw_h_generado'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    # Pie chart: distribución de proyectos por condición (si existe columna)
    if 'condicion' in data.columns:
        st.subheader("🥧 Distribución de proyectos por condición")
        condicion_data = data['condicion'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(condicion_data, labels=condicion_data.index, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    conn.close()
else:
    st.error("❌ No se encontró el archivo SectorMineroEnergeticoColombia.db. Asegúrate de subirlo al repositorio.")
