import streamlit as st
import pandas as pd

ruta_zni = 'DATAX\ZNI.csv'

ruta_divipola = 'DATAX\DIVIPOLA.csv'

df_zni = pd.read_csv(ruta_zni)
df_divipola = pd.read_csv(ruta_divipola)

## ==================================================================
# TRAER NOMBRE OFICIAL DEL DEPARTAMENTO
df_zni = df_zni.merge(
    df_divipola[['Código Departamento','Nombre_departamento']].drop_duplicates('Código Departamento'),
    left_on='ID DEPATAMENTO',
    right_on='Código Departamento',
    how='left'
)

st.text(df_zni)

df_zni['DEPARTAMENTO'] = df_zni['Nombre_departamento']
df_zni = df_zni.drop(columns=['Código Departamento','Nombre_departamento'])

## ==================================================================
# TRAER NOMBRE OFICIAL DEL MUNICIPIO
df_zni = df_zni.merge(
    df_divipola[['Codigo Municipio','Nombre Municipio']].drop_duplicates('Codigo Municipio'),
    left_on='ID MUNICIPIO',
    right_on='Codigo Municipio',
    how='left'
)

st.text(df_zni)

df_zni['MUNICIPIO'] = df_zni['Nombre Municipio']
df_zni = df_zni.drop(columns=['Codigo Municipio','Nombre Municipio'])

## =================================================================
# TRAER NOMBRE OFICIAL DE LA LOCALIDAD (Centro Poblado)
df_zni = df_zni.merge(
    df_divipola[['Código Centro Poblado','Nombre Centro Poblado']].drop_duplicates('Código Centro Poblado'),
    left_on='ID LOCALIDAD',
    right_on='Código Centro Poblado',
    how='left'
)

st.text(df_zni)

df_zni['LOCALIDAD'] = df_zni['Nombre Centro Poblado']
df_zni = df_zni.drop(columns=['Código Centro Poblado','Nombre Centro Poblado'])

st.text(df_zni)

## =================================================================
# CORREGIR NOMBRES DE LOS DIAS
## Todos a Mayúscula
df_zni['DÍA DE DEMANDA MÁXIMA'] = df_zni['DÍA DE DEMANDA MÁXIMA'].str.upper()
st.text(df_zni)

## Listado de SIN y CON tildes
viejos = ['MIERCOLES','SABADO']
nuevos = ['MIÉRCOLES','SÁBADO']

st.text(df_zni)

## Crear un DICCIONARIO con las listas EMPAQUETADAS
reemplazos = dict(zip(viejos, nuevos))

st.text(df_zni)

## Otra forma 1
# reemplazos = dict([['MIERCOLES', 'MIÉRCOLES'],['SABADO','SÁBADO']])

## Otra forma 2
# reemplazos = {
#     'MIERCOLES': 'MIÉRCOLES',
#     'SABADO': 'SÁBADO'
# }

## Reemplazar usando los diccionarios
df_zni['DÍA DE DEMANDA MÁXIMA'] = df_zni['DÍA DE DEMANDA MÁXIMA'].replace(reemplazos, regex=True)

st.text(df_zni)

## =================================================================
# Eliminar TODOS los registros con valores nulos Y ALMACENAR en el mismo dataframe (inplace=True)
df_zni.dropna(inplace = True)

# CORREGIR PROBLEMAS CON COLUMNAS NUMÉRICAS QUE SON OBJECT
df_zni['ENERGÍA ACTIVA'] = df_zni['ENERGÍA ACTIVA'].str.replace('.', '', regex=False).astype(int)

df_zni['ENERGÍA REACTIVA'] = df_zni['ENERGÍA REACTIVA'].str.replace('.', '', regex=False).astype(int)

df_zni['POTENCIA MÁXIMA'] = df_zni['POTENCIA MÁXIMA'].str.replace('.', '', regex=False)
df_zni['POTENCIA MÁXIMA'] = df_zni['POTENCIA MÁXIMA'].str.replace(',', '.', regex=False).astype(float).astype(int)

st.text(df_zni)

# AGRUPAR LOS DATOS POR DEPARTAMENTO Y POR MUNICIPIO
# SUMANDO LOS VALORES DE ENERGÍA ACTIVA Y REACTIVA
df_agrupado = df_zni.groupby(['DEPARTAMENTO','MUNICIPIO'])[['ENERGÍA ACTIVA', 'ENERGÍA REACTIVA']].sum()

st.text(df_zni)


df_pivote = df_zni.pivot_table(
    index = 'LOCALIDAD',
    columns = 'AÑO SERVICIO',
    values = 'ENERGÍA ACTIVA',
    aggfunc='sum'
)

st.text(df_zni)

#CONFIGURACION STREAMLIT====


### VISUALIZACION DE DATOS========

