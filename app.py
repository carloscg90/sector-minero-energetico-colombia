
import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt

st.markdown("<h1 style='text-align: center;'>⚡ Dashboard Sector Minero Energético Colombia</h1>", unsafe_allow_html=True)

db_path = "SectorMineroEnergeticoColombia.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)

    st.subheader("📋 Tabla eficiencia_energetica")
    data = pd.read_sql_query("SELECT * FROM eficiencia_energetica", conn)
    st.dataframe(data)

    st.subheader("📊 Energía generada por proyecto")
    energia = data.groupby('proyecto_id')['kw_h_generado'].sum()
    st.bar_chart(energia)

    st.subheader("💰 Proyectos con Inversión superior al umbral")
    umbral = st.slider("Selecciona el monto mínimo de inversión", min_value=0, max_value=10000000, step=500000, value=2000000)

    query = f"""
        SELECT sub.nombre, sub.total_inversion
        FROM (
            SELECT p.nombre, SUM(i.monto) AS total_inversion
            FROM proyectos p
            JOIN inversiones i ON p.id_proyecto = i.proyecto_id
            GROUP BY p.nombre
        ) sub
        WHERE sub.total_inversion > {umbral};
    """
    df_inversiones = pd.read_sql_query(query, conn)
    st.dataframe(df_inversiones)

    if not df_inversiones.empty:
        # Gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(df_inversiones['nombre'], df_inversiones['total_inversion'], color='orange')
        ax.set_ylabel("Inversión Total")
        ax.set_title(f"Inversiones por proyecto > {umbral:,} COP")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        # Gráfico de torta
        st.subheader("🥧 Distribución de inversión por proyecto")
        fig2, ax2 = plt.subplots()
        ax2.pie(df_inversiones['total_inversion'], labels=df_inversiones['nombre'], autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)
    else:
        st.info("🔍 No hay proyectos con inversión mayor al umbral seleccionado.")

    conn.close()
else:
    st.error("❌ No se encontró el archivo SectorMineroEnergeticoColombia.db. Asegúrate de subirlo al repositorio.")
