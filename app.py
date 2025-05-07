
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Distribución de kWh Generado por Proyecto")

# Cargar datos desde CSV
df = pd.read_csv("datos_energia.csv")

# Agrupar por nombre del proyecto
df_grouped = df.groupby('nombre')['kw_h_generado'].sum().reset_index()

# Selector de top N
top_n = st.slider("Selecciona el número de proyectos a mostrar", 1, len(df_grouped), 5)

# Top N
df_top = df_grouped.sort_values(by='kw_h_generado', ascending=False).head(top_n)

# Pie chart
fig, ax = plt.subplots()
ax.pie(df_top['kw_h_generado'], labels=df_top['nombre'], autopct='%1.1f%%', startangle=140)
ax.axis('equal')
plt.title(f"Top {top_n} Proyectos por kWh Generado")
st.pyplot(fig)
