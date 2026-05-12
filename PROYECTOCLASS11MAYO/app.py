import streamlit as st
import pandas as pd

## CARGA DE DATOS===========
ruta = 'DATAX/Estado_de_la_prestación_del_servicio_de_energía_en_Zonas_No_Interconectadas_20260422.csv'
df = pd.read_csv(ruta)

##ANALISIS DE DATOS====
filas = df.shape[0]
columnas = df.shape[1]


### VISUALZIACION DE DATOS======

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader('Número de Filas')
        st.text(filas)

with col2:
    with st.container(border=True):
        st.subheader('Número de Columnas')
        st.text(columnas)

## OTRA FORMA DE MOSTRAR INDICADORES
col3, col4 = st.columns(2)
with col3:
        st.metric('Numero de filas', filas, border=True)
with col4:
       st.metric('Numero de filas', filas, border=True)

print("Hola Mundo")
