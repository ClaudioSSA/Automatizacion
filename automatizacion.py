# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import base64
import io
from datetime import datetime
from datetime import date
import sqlite3



def cargar_datos_como_dataframe():
    conn = sqlite3.connect('datos_concursos.db')
    c = conn.cursor()

    c.execute('SELECT * FROM concursos')
    datos = c.fetchall()

    # Convertir los datos en un DataFrame
    column_names = ["id", "Concurso", "Unidad_Requirente", "Nombre_Responsable", "fecha_solicitud_ddo",
                    "fecha_solicitud_rs", "fecha_solicitud_extracto_legal", "fecha_publicacion_adquisiciones",
                    "fecha_publicacion_extracto_legal", "fecha_termino_publicacion", "fecha_envio_cv",
                    "fecha_devolucion_unidad", "fecha_evaluacion_psicolaboral", "fecha_envio_informes",
                    "fecha_decision_seleccionado", "fecha_ingreso"]

    df = pd.DataFrame(datos, columns=column_names)

    # Convertir columnas de fecha a tipo datetime si aún no lo están
    columnas_fecha = ['fecha_solicitud_ddo', 'fecha_solicitud_rs', 'fecha_solicitud_extracto_legal',
                      'fecha_publicacion_adquisiciones', 'fecha_publicacion_extracto_legal',
                      'fecha_termino_publicacion', 'fecha_envio_cv', 'fecha_devolucion_unidad',
                      'fecha_evaluacion_psicolaboral', 'fecha_envio_informes', 'fecha_decision_seleccionado',
                      'fecha_ingreso']
    
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    conn.close()
    return df

def generar_alertas(df):
    # Calcular los tiempos entre etapas del procedimiento
    df['Tiempo_Apertura_a_Solicitud_Extracto'] = df['fecha_solicitud_extracto_legal'] - df['fecha_solicitud_ddo']
    df['Tiempo_Solicitud_a_Publicacion_Extracto'] = df['fecha_publicacion_extracto_legal'] - df['fecha_solicitud_extracto_legal']
    df['Tiempo_Cierre_Concurso_a_Envio_CV'] = df['fecha_envio_cv'] - df['fecha_termino_publicacion']
    df['Tiempo_Entrevista_Envio_Informe'] = df['fecha_envio_informes'] - df['fecha_evaluacion_psicolaboral']
    df['Tiempo_Envio_Informe_Respuesta_Adjudicacion'] = df['fecha_decision_seleccionado'] - df['fecha_envio_informes']

    # Gráficos de los tiempos usando Seaborn
    plt.figure(figsize=(14, 8))

    # Gráfico 1: Tiempo desde Apertura del concurso hasta Solicitud de publicación en Extracto Legal
    plt.subplot(2, 3, 1)
    sns.histplot(df['Tiempo_Apertura_a_Solicitud_Extracto'].dt.days, bins=20, color='skyblue')
    plt.title('Tiempo Apertura a Solicitud Extracto Legal')
    plt.xlabel('Días')
    plt.ylabel('Frecuencia')

    # Gráfico 2: Tiempo desde Solicitud de Extracto Legal hasta Publicación en Extracto Legal
    plt.subplot(2, 3, 2)
    sns.histplot(df['Tiempo_Solicitud_a_Publicacion_Extracto'].dt.days, bins=20, color='salmon')
    plt.title('Tiempo Solicitud a Publicación Extracto Legal')
    plt.xlabel('Días')
    plt.ylabel('Frecuencia')

    # ... (Agregar gráficos para los otros tiempos)

    plt.tight_layout()

    # Indicadores anuales
    df['Año'] = df['fecha_solicitud_ddo'].dt.year
    indicadores_anuales = df.groupby('Año').size()  # Cantidad de concursos por año

    # Gráficos de totalidad de procesos desarrollados anualmente
    plt.figure(figsize=(10, 6))
    sns.barplot(x=indicadores_anuales.index, y=indicadores_anuales.values, palette='viridis')
    plt.title('Cantidad de concursos por año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de concursos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Gráficos de cantidad de concursos por solicitantes
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Unidad_Requirente', palette='muted', order=df['Unidad_Requirente'].value_counts().index)
    plt.title('Cantidad de concursos por solicitantes')
    plt.xlabel('Solicitantes')
    plt.ylabel('Cantidad de concursos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

    return indicadores_anuales

# Suponiendo que tienes un DataFrame llamado 'datos_concursos'
datos_concursos = cargar_datos_como_dataframe()

# Generar alertas e indicadores
resultados_alertas = generar_alertas(datos_concursos)









if "edicion_exitosa" not in st.session_state:
    st.session_state.edicion_exitosa = False  # Inicializar la bandera de edición exitosa
    



#Funcion para calcular el tiempo entre dos etapas cualquiera
def calcular_tiempo_entre_etapas(df, etapa_inicio, etapa_fin):
    try:
        # Acceder a las fechas correspondientes
        fecha_inicio = df[etapa_inicio]
        fecha_fin = df[etapa_fin]

        # Calcular la diferencia de tiempo
        diferencia_tiempo = fecha_fin - fecha_inicio

     # En lugar de plt.show(), usamos st.pyplot()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(diferencia_tiempo, marker='o')
        ax.set_xlabel('Índice de Procesos')
        ax.set_ylabel('Días Transcurridos')
        ax.set_title(f'Tiempo entre {etapa_inicio} y {etapa_fin}')
        ax.grid(True)

        # Mostramos el gráfico usando st.pyplot()
        st.pyplot(fig)
        
    except KeyError as e:
        print(f"Error: No se encontraron columnas con los nombres '{etapa_inicio}' y '{etapa_fin}' en el DataFrame.")
        return None
    except Exception as e:
        print(f"Error al calcular y visualizar el tiempo entre etapas: {str(e)}")
        return None


def calcular_tiempo_entre_etapas(df, etapa_inicio, etapa_fin):
    try:
        # Acceder a las fechas correspondientes
        fecha_inicio = df[etapa_inicio]
        fecha_fin = df[etapa_fin]

        # Calcular la diferencia de tiempo
        diferencia_tiempo = fecha_fin - fecha_inicio

        # Visualizar en un gráfico
        plt.figure(figsize=(8, 6))
        plt.plot(diferencia_tiempo, marker='o')
        plt.xlabel('Índice de Procesos')
        plt.ylabel('Días Transcurridos')
        plt.title(f'Tiempo entre {etapa_inicio} y {etapa_fin}')
        plt.grid(True)
        plt.show()
        
    except KeyError as e:
        print(f"Error: No se encontraron columnas con los nombres '{etapa_inicio}' y '{etapa_fin}' en el DataFrame.")
        return None
    except Exception as e:
        print(f"Error al calcular y visualizar el tiempo entre etapas: {str(e)}")
        return None

# Nueva función para clasificar por mes
def clasificar_por_mes(datos_cargados):
    # Convertir a DataFrame
    df = pd.DataFrame(datos_cargados)

    # Convertir la columna 'fecha_solicitud_ddo' a tipo datetime si aún no está en ese formato
    df['fecha_solicitud_ddo'] = pd.to_datetime(df['fecha_solicitud_ddo'])

    # Crear nueva columna 'mes' basada en la fecha de solicitud al DDO
    df['mes'] = df['fecha_solicitud_ddo'].dt.strftime('%Y-%m')

    return df


def reindexar_ids():
    conn = sqlite3.connect('datos_concursos.db')
    c = conn.cursor()

    # Obtener los datos ordenados por ID
    c.execute('SELECT * FROM concursos ORDER BY id')
    datos = c.fetchall()

    # Actualizar los IDs en la base de datos
    for idx, dato in enumerate(datos, start=1):
        c.execute('UPDATE concursos SET id=? WHERE id=?', (idx, dato[0]))

    conn.commit()
    conn.close()

def eliminar_fila_de_base_de_datos(id_a_eliminar):
    try:
        conn = sqlite3.connect('datos_concursos.db')
        c = conn.cursor()

        delete_query = f"DELETE FROM concursos WHERE id = {id_a_eliminar}"
        c.execute(delete_query)

        conn.commit()
        conn.close()
    
        reindexar_ids()
        
        return True  # Indica que la eliminación fue exitosa

    except sqlite3.Error as e:
        print(f"Error de SQLite al eliminar la fila de la base de datos: {str(e)}")
        return False  # Indica que hubo un error de SQLite

    except Exception as e:
        print(f"Error al eliminar la fila de la base de datos: {str(e)}")
        return False  # Indica que hubo un error al eliminar

# Verificar si es una fecha y obtener el valor correspondiente
def obtener_valor_fecha(valor):
    # Verificar si el valor es de tipo fecha
    if isinstance(valor, str) and valor.strip():
        try:
            fecha = datetime.strptime(valor.strip(), "%Y-%m-%d").date()
            return fecha
        except ValueError:
            return None
    elif isinstance(valor, date):
        return valor
    else:
        return None
   

def obtener_valor_texto(valor):
    # Verificar si el valor es de tipo texto
    if isinstance(valor, str) and valor.strip():  # Asumiendo que los textos son strings no vacíos
        return valor.strip()  # Devuelve la cadena sin espacios alrededor
    else:
        return None  # Si no es un texto válido, devuelve None



# Función para cargar datos desde la base de datos
def cargar_datos():
    conn = sqlite3.connect('datos_concursos.db')
    c = conn.cursor()

    c.execute('SELECT * FROM concursos')
    datos = c.fetchall()

    # Convertir los datos en un formato adecuado para su uso
    datos_formateados = []
    for dato in datos:
        datos_formateados.append({
            "id": dato[0],  # Se agrega el id como primer elemento
            "Concurso": dato[1],
            "Unidad_Requirente": dato[2],
            "Nombre_Responsable": dato[3],
            "fecha_solicitud_ddo": dato[4],
            "fecha_solicitud_rs": dato[5],
            "fecha_solicitud_extracto_legal": dato[6],
            "fecha_publicacion_adquisiciones": dato[7],
            "fecha_publicacion_extracto_legal": dato[8],
            "fecha_termino_publicacion": dato[9],
            "fecha_envio_cv": dato[10],
            "fecha_devolucion_unidad": dato[11],
            "fecha_evaluacion_psicolaboral": dato[12],
            "fecha_envio_informes": dato[13],
            "fecha_decision_seleccionado": dato[14],
            "fecha_ingreso": dato[15]
        })

    conn.close()
    return datos_formateados


def editar_datos():
    print("La función editar_datos() se está ejecutando...")
    st.header("Editar Datos")

    # Cargar datos desde la base de datos
    datos_cargados = cargar_datos()

    if len(datos_cargados) > 0:
        df = pd.DataFrame(datos_cargados)

        fila_editar = st.number_input("Ingrese el número de fila que desea editar", min_value=1, max_value=len(df), step=1)

        if fila_editar > 0 and fila_editar <= len(df):
            st.subheader("Editar Datos")

            # Mostrar los datos actuales de la fila seleccionada
            st.write("Datos actuales:")
            st.write(df.iloc[fila_editar - 1])

            # Crear un formulario para editar los campos existentes y vacíos
            st.subheader("Editar datos existentes y campos vacíos:")

            edicion_realizada = False  # Variable para controlar si se realizó alguna edición
            datos_actualizados = {}  # Diccionario para almacenar los cambios

            for column in df.columns:
                valor_actual = df.at[fila_editar - 1, column]

                if pd.isnull(valor_actual):  # Verificar si el campo está vacío
                    if column in ["Concurso", "Unidad_Requirente", "Nombre_Responsable"]:  # Si es texto
                        nuevo_valor = st.text_input(f"Editar {column} en fila {fila_editar}", value="")
                        nuevo_valor = obtener_valor_texto(nuevo_valor)
                    elif column.startswith("fecha"):  # Si es una fecha
                        nuevo_valor = st.date_input(f"Editar {column} en fila {fila_editar}", value=None)
                    else:
                        nuevo_valor = st.text_input(f"Editar {column} en fila {fila_editar}", value="")

                    datos_actualizados[column] = nuevo_valor  # Almacena el valor actualizado

                else:  # Si el campo ya tiene un valor
                    if column in ["Concurso", "Unidad_Requirente", "Nombre_Responsable"]:  # Si es texto
                        nuevo_valor = st.text_input(f"Editar {column} en fila {fila_editar}", value=valor_actual)
                        nuevo_valor = obtener_valor_texto(nuevo_valor)
                    elif column.startswith("fecha"):  # Si es una fecha
                        nuevo_valor = st.date_input(f"Editar {column} en fila {fila_editar}", value=obtener_valor_fecha(valor_actual))
                    else:
                        nuevo_valor = st.text_input(f"Editar {column} en fila {fila_editar}", value=valor_actual)

                    # Actualizar el valor en el DataFrame si se ingresa uno nuevo
                    if nuevo_valor != valor_actual:
                        df.at[fila_editar - 1, column] = nuevo_valor
                        edicion_realizada = True
                        datos_actualizados[column] = nuevo_valor

            # Botón para guardar los cambios
            if st.button("Guardar Cambios"):
                if edicion_realizada:  # Verificar si se realizaron ediciones antes de guardar
                    # Obtener el ID de la fila a editar
                    id_a_editar = df.at[fila_editar - 1, "id"]

                    # Actualizar la base de datos con los cambios
                    actualizar_dato_en_base_de_datos(id_a_editar, datos_actualizados)

                    # Mostrar mensaje de éxito
                    st.success("Cambios guardados exitosamente.")

                    # Mostrar datos actualizados en Streamlit
                    st.write("Datos actualizados:")
                    st.write(df.iloc[fila_editar - 1])

                else:
                    st.warning("No se detectó ninguna edición. No hay cambios para guardar.")

            # Botón para eliminar la fila
            if st.button("Eliminar Fila"):
                if fila_editar > 0 and fila_editar <= len(df):
                    id_a_eliminar = df.at[fila_editar - 1, "id"]
                    if eliminar_fila_de_base_de_datos(id_a_eliminar):
                        st.success("Fila eliminada exitosamente.")
                        # Recargar los datos después de la eliminación y mostrarlos
                        datos_cargados = cargar_datos()
                        # Mostrar los datos actualizados en Streamlit
                        # ...

                    else:
                        st.error("Error al eliminar la fila.")
                else:
                    st.warning("Ingrese un número de fila válido.")

        else:
            st.warning("Ingrese un número de fila válido.")

    else:
        st.info("Aún no se han ingresado datos.")




def validar_fecha(fecha, nombre_campo):
    if fecha is not None and not pd.isnull(fecha):
        return st.date_input(nombre_campo, value=fecha)
    return None

def obtener_alertas_cercanas(datos_cargados):
    today = datetime.now().date()
    alertas_cercanas = []

    for dato in datos_cargados:
        concurso = dato.get("Concurso")
        unidad_requirente = dato.get("Unidad_Requirente")
        
        for fecha_columna in ['fecha_devolucion_unidad', 'fecha_envio_informes', 'fecha_decision_seleccionado']:
            fecha_str = dato.get(fecha_columna)
            if fecha_str:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                diferencia_dias = (fecha - today).days
                if 0 <= diferencia_dias <= 3:  # Considera fechas hasta 3 días en el futuro
                    alertas_cercanas.append({
                        "ID": dato["id"],
                        "Concurso": concurso,
                        "Unidad Requirente": unidad_requirente,
                        "Fecha": fecha_columna.replace('_', ' '),
                        "Fecha límite": fecha.strftime("%Y-%m-%d")
                    })

    # Construye el DataFrame dentro de la función
    df_alertas = pd.DataFrame(alertas_cercanas)
    
    # Ahora puedes usar df_alertas para cualquier otra manipulación dentro de la función
    # Por ejemplo, generar gráficos, cálculos adicionales, etc.

    return df_alertas  # Retorna el DataFrame


    
datos_ingresados = []
# Función para actualizar un dato en la base de datos


def actualizar_dato_en_base_de_datos(id, datos_actualizados):
    try:
        conn = sqlite3.connect('datos_concursos.db')
        c = conn.cursor()

        update_query = "UPDATE concursos SET "
        values = []

        for column, value in datos_actualizados.items():
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            values.append(f"{column} = '{value}'")

        update_query += ", ".join(values)
        update_query += f" WHERE id = {id}"
        
        c.execute(update_query)

        conn.commit()
        conn.close()
        return True  # Indica que la actualización fue exitosa

    except sqlite3.Error as e:
        print(f"Error de SQLite al actualizar datos en la base de datos: {str(e)}")
        return False  # Indica que hubo un error de SQLite

    except Exception as e:
        print(f"Error al actualizar datos en la base de datos: {str(e)}")
        return False  # Indica que hubo un error al actualizar



# Función para guardar datos en la base de datos
def guardar_datos(datos):
    try:
        conn = sqlite3.connect('datos_concursos.db')
        c = conn.cursor()

        for dato in datos:
            c.execute('''
                INSERT INTO concursos (
                    Concurso, Unidad_Requirente, Nombre_Responsable, fecha_solicitud_ddo, fecha_solicitud_rs,
                    fecha_solicitud_extracto_legal, fecha_publicacion_adquisiciones, fecha_publicacion_extracto_legal,
                    fecha_termino_publicacion, fecha_envio_cv, fecha_devolucion_unidad, fecha_evaluacion_psicolaboral,
                    fecha_envio_informes, fecha_decision_seleccionado, fecha_ingreso
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(dato.values()))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al guardar datos en la base de datos: {str(e)}")
        return False

# Función para cargar datos desde la base de datos


def calcular_diferencia_fechas(fecha_inicial, fecha_final):
    # Convierte las fechas a objetos datetime
    fecha_inicial = datetime.strptime(fecha_inicial, "%Y-%m-%d")
    fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")

    # Calcula la diferencia de tiempo
    diferencia = fecha_final - fecha_inicial
    return diferencia.days, diferencia.total_seconds() / 3600  # Diferencia en días y horas
# Entre fecha_solicitud_ddo y fecha solicitu extracto legal
def visualizar_tiempo_entre_fechas():
    datos_cargados = cargar_datos()

    if datos_cargados:
        fechas = []
        for dato in datos_cargados:
            fecha_solicitud_ddo = dato.get("fecha_solicitud_ddo")
            fecha_solicitud_extracto_legal = dato.get("fecha_solicitud_extracto_legal")
            
            if fecha_solicitud_ddo and fecha_solicitud_extracto_legal:
                # Calcula la diferencia de tiempo
                dias, horas = calcular_diferencia_fechas(fecha_solicitud_ddo, fecha_solicitud_extracto_legal)
                fechas.append((dias, horas))
        
        if fechas:
            # Prepara los datos para el gráfico
            procesos = [f"Proceso {i+1}" for i in range(len(fechas))]
            dias = [fecha[0] for fecha in fechas]
            horas = [fecha[1] for fecha in fechas]

            # Crea el gráfico
            plt.figure(figsize=(8, 6))
            plt.bar(procesos, dias, color='skyblue')
            plt.xlabel("Proceso")
            plt.ylabel("Días")
            plt.title("Tiempo entre Apertura del concurso y Solicitud de publicación en Extracto Legal")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Muestra el gráfico
            plt.show()
        else:
            print("No hay datos suficientes para generar el gráfico.")
    else:
        print("No hay datos disponibles en la base de datos.")



# Título de la aplicación y logo
st.image("utem.jpg", width=150)
st.title("Registro de Concursos de Reclutamiento y Selección UTEM")

# Menú de navegación
pagina_seleccionada = st.sidebar.selectbox("Selecciona una página", ["Dashboard","Ingreso de datos","Visualizar Datos","Editar datos","Clasificar por Mes","Visualizar Graficos","Alertas cercanas"])

if pagina_seleccionada == "Dashboard":
    st.header("Bienvenido al dashboard")
    

    mi_dataframe = pd.DataFrame()
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_envio_informes', 'fecha_decision_seleccionado')
    mi_dataframe = cargar_datos_como_dataframe()
    st.table(mi_dataframe)
    # Suponiendo que tienes tu DataFrame cargado como mi_dataframe
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_solicitud_ddo', 'fecha_solicitud_extracto_legal')
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_solicitud_extracto_legal', 'fecha_publicacion_extracto_legal')
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_termino_publicacion', 'fecha_envio_cv')
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_evaluacion_psicolaboral', 'fecha_envio_informes')
    calcular_tiempo_entre_etapas(mi_dataframe, 'fecha_envio_informes', 'fecha_decision_seleccionado')



    



   
def visualizar_graficos():
    # Cargar datos desde la base de datos
    datos_cargados = cargar_datos()

    unidades_requirentes = [dato["Unidad_Requirente"] for dato in datos_cargados]

    # Verificar si hay datos disponibles
    if not unidades_requirentes:
        st.subheader("Porcentaje de Solicitudes por Unidad Requirente")
        st.warning("Aún no hay datos registrados.")
    else:
        st.subheader("Porcentaje de Solicitudes por Unidad Requirente")
        df = pd.DataFrame(unidades_requirentes, columns=["Unidad Requirente"])
        counts = df["Unidad Requirente"].value_counts(normalize=True) * 100
        fig, ax = plt.subplots(figsize=(8, 6))  # Modifica el tamaño del gráfico aquí (ancho x alto)
        counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Porcentaje")
        ax.set_xlabel("Unidad Requirente")
        ax.set_title("Porcentaje de Solicitudes por Unidad Requirente")
        
        # Crear un enlace para descargar el gráfico
        st.pyplot(fig)
        data = get_image_download_link(fig, 'mi_grafico.png')
        st.markdown(data, unsafe_allow_html=True)

def get_image_download_link(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:file/png;base64,{data}" download="{filename}">Descargar Gráfico</a>'
    return href

# Función para visualizar el porcentaje de solicitudes por unidad requirente
def visualizar_porcentaje_solicitudes():
    # Cargar datos desde la base de datos
    datos_cargados = cargar_datos()

    if datos_cargados:
        df = pd.DataFrame(datos_cargados, columns=["Unidad_Requirente"])
        counts = df["Unidad_Requirente"].value_counts(normalize=True) * 100
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Porcentaje")
        ax.set_xlabel("Unidad Requirente")
        ax.set_title("Porcentaje de Solicitudes por Unidad Requirente")
        return fig
    else:
        # No hay datos cargados, mostrar un mensaje de advertencia o manejar la situación como prefieras
        st.warning("Aún no hay datos registrados para visualizar el porcentaje de solicitudes por unidad requirente.")
        return None  # O podrías retornar alguna información específica para manejar el caso sin datos


# Contenido de las páginas
if pagina_seleccionada == "Ingreso de datos":
    # Contenido de la página de inicio (formulario y datos ingresados)
    st.header("Ingrese los datos al formulario de concursos")

    # Formulario para ingresar datos
    concurso = st.text_input("Nombre del concurso")
    unidad_requirente = st.text_input("Unidad Requirente")
    nombre_responsable = st.text_input("Nombre del Responsable")
    fecha_solicitud_ddo = st.date_input("Fecha de Solicitud al DDO", None)
    fecha_solicitud_rs = st.date_input("Fecha de Solicitud a la Unidad de R&S", None)
    fecha_solicitud_extracto_legal = st.date_input("Fecha de Solicitud de Extracto Legal", None)
    fecha_publicacion_adquisiciones = st.date_input("Fecha de Publicación Unidad de Adquisiciones", None)
    fecha_publicacion_extracto_legal = st.date_input("Fecha de Publicación Extracto Legal y Trabajando.com", None)
    fecha_termino_publicacion = st.date_input("Fecha de Término de Publicación", None)
    fecha_envio_cv = st.date_input("Fecha de Envío de C. Vitae", None)
    fecha_devolucion_unidad = st.date_input("Fecha de Devolución a la Unidad", None)
    fecha_evaluacion_psicolaboral = st.date_input("Fecha de Evaluación Psicolaboral", None)
    fecha_envio_informes = st.date_input("Fecha de Envío de Informes", None)
    fecha_decision_seleccionado = st.date_input("Fecha de Decisión del Seleccionado", None)
    fecha_ingreso = st.date_input("Fecha de Ingreso", None)

    # Botón para guardar los datos ingresados
    if st.button("Guardar Datos"):
        # Crear un diccionario con los datos ingresados
        nuevo_dato = {
            "Concurso": concurso,
            "Unidad_Requirente": unidad_requirente,
            "Nombre_Responsable": nombre_responsable,
            "fecha_solicitud_ddo": fecha_solicitud_ddo,
            "fecha_solicitud_rs": fecha_solicitud_rs,
            "fecha_solicitud_extracto_legal": fecha_solicitud_extracto_legal,
            "fecha_publicacion_adquisiciones": fecha_publicacion_adquisiciones,
            "fecha_publicacion_extracto_legal": fecha_publicacion_extracto_legal,
            "fecha_termino_publicacion": fecha_termino_publicacion,
            "fecha_envio_cv": fecha_envio_cv,
            "fecha_devolucion_unidad": fecha_devolucion_unidad,
            "fecha_evaluacion_psicolaboral": fecha_evaluacion_psicolaboral,
            "fecha_envio_informes": fecha_envio_informes,
            "fecha_decision_seleccionado": fecha_decision_seleccionado,
            "fecha_ingreso": fecha_ingreso,
        }

        # Guardar el nuevo dato en la lista
        datos_ingresados.append(nuevo_dato)

        # Guardar datos en el archivo
       #guardar_datos(datos_ingresados)
        guardar_datos([nuevo_dato])

        # Mostrar mensaje de éxito
        st.success("Datos ingresados correctamente.")

if pagina_seleccionada == "Visualizar Datos":
    st.header("Datos Ingresados")
    
    # Cargar datos desde la base de datos
    datos_cargados = cargar_datos()

    if len(datos_cargados) > 0:
        df = pd.DataFrame(datos_cargados)
        # Eliminar la columna 'Fechas de ingreso' si existe
        if 'Fechas de ingreso' in df.columns:
            df = df.drop(columns=['Fechas de ingreso'], errors='ignore')
        
        # Mostrar el DataFrame en Streamlit
        st.table(df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', 'lightblue'), ('color', 'black')]},
            {'selector': 'td', 'props': [('background-color', 'lightgrey'), ('color', 'black')]}
        ]).set_properties(**{'text-align': 'left'}).set_table_attributes('border="1"').set_table_styles([{'selector': 'tr', 'props': [('font-size', '8pt')]}]))

        # Mostrar mensaje de éxito tras la edición
        if st.session_state.edicion_exitosa:
            st.success("Datos editados correctamente.")
            st.session_state.edicion_exitosa = False  # Reiniciar la bandera después de mostrar el mensaje
    else:
        st.info("Aún no se han ingresado datos.")
        
        
if pagina_seleccionada == "Clasificar por Mes":
    datos_cargados = cargar_datos()
    
    if datos_cargados:
        df_meses = clasificar_por_mes(datos_cargados)
        st.header("Datos Clasificados por Mes")

        for mes, datos_mes in df_meses.groupby('mes'):
            st.subheader(f"Mes: {mes}")
            st.dataframe(datos_mes)
    else:
        st.warning("Aún no hay datos ingresados.")
       

elif pagina_seleccionada == "Visualizar Graficos":
    pag_seleccionada = st.sidebar.selectbox("Selecciona una página", ["Visualizar tiempo entre fechas", "Visualizar Graficos"])
    if pag_seleccionada == "Visualizar tiempo entre fechas":
        visualizar_tiempo_entre_fechas()
        #calcular_tiempo_entre_etapas()
    elif pag_seleccionada == "Visualizar Graficos":
        visualizar_graficos()
        
        
elif pagina_seleccionada == "Editar datos":
    editar_datos()
    
    
    
    

elif pagina_seleccionada == "Alertas cercanas":
    # Suponiendo que tienes un DataFrame df_alertas con tus datos

    st.header("Alertas de fechas cercanas")

    # Cargar datos desde la base de datos
    datos_cargados = cargar_datos()

    # Llamas a la función para obtener df_alertas
    df_alertas = obtener_alertas_cercanas(datos_cargados)

    if df_alertas.empty:
        st.info("No hay alertas cercanas.")
    else:
        # Muestra el DataFrame en Streamlit
        st.write(df_alertas)





