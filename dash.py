import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
page_title="Dashboard de Ventas",page_icon="📊",
layout="centered")
st.title("Ventas trimestre I de 2024")
df=pd.read_excel("ventas_supermercado.xlsx", skiprows=0,header=0)
st.write(df.head())
# Cambiar el formato a los números
def formato(numero):
    """Convierte número a formato: 1.234.567,89"""
    return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Calcular KPIs
total_ventas = df['Total'].sum()
ingreso_bruto = df['Ingreso bruto'].sum()
promedio_calificacion = df['Calificación'].mean()

# Mostrar KPIs en columnas con formato personalizado
st.metric("🛒 Total Ventas", f"{formato(total_ventas)}")
st.metric("💰 Ingreso Bruto", f"{formato(ingreso_bruto)}")
st.metric("⭐ Calificación Promedio", f"{promedio_calificacion:.2f}")


col1, col2, col3= st.columns([3,3,1])
with col1:
    st.metric("total ventas",f"${formato(total_ventas)}")
with col2:
    st.metric("total ventas",f"${formato(ingreso_bruto)}")
with col3:
    st.metric("total ventas",f"${formato(promedio_calificacion)}")


with st.sidebar:
    st.header("Filtros")
    ciudades= st.multiselect("Selecciona ciudades: ", df["Ciudad"].unique(),default=df["Ciudad"].unique())
    lineas=st.multiselect("selecciona líneas de productos", df["Línea de producto"].unique(),default=df["Línea de producto"].unique())

# FILTRAR LOS DATOS

df_filtrado= df[df["Ciudad"].isin(ciudades) & df["Línea de producto"].isin(lineas)]
tab1, tab2, tab3= st.tabs(["Ventas por mes", "Por linea", "Datos"], width="stretch")
with tab1:
    st.subheader("Ventas por mes")
    df_filtrado["Mes"]= df_filtrado["Fecha"].dt.to_period("M").astype(str)
    df_filtrado["Mes"]= df_filtrado["Fecha"].dt.strftime("%m-%Y")

    ventas_mes= df_filtrado.groupby("Mes")["Total"].sum().sort_index()

    fig1, ax1=plt.subplots()
    ventas_mes.plot(kind="line", marker="o", ax=ax1, color="teal", title="tendencias de ventas mensulaes")

    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Total ventas")
    ax1.grid("True")
    plt.xticks(rotation=45)
    st.pyplot(fig1)


with tab2:
    st.subheader("Ventas por linea de producto")
    ventas_linea=df_filtrado.groupby("Línea de producto")["Total"].sum().sort_values()
    fig2, ax2=plt.subplots()
    ventas_linea.plot(kind="barh", ax=ax2, color="orange", title="Ventas por linea de producto ")

    ax2.set_ylabel("")
    ax2.set_xlabel("Ventas")
    st.pyplot(fig2)

df_filtrado.reset_index(drop=True, inplace=True)
df_filtrado.index = df_filtrado.index + 1


with tab3:
    st.subheader("Datos")
    st.dataframe(df_filtrado)
    # exportar a excel en memoria
    output= BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name="Ventas")

    st.download_button(
    label="descarga los datos en excel",data= output.getvalue(),file_name="Ventas_filtradas.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )





