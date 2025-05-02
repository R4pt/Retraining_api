import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(
    page_title="Predictor de Depósitos Bancarios",
    page_icon="💰",
    layout="wide",
)

st.title("🏦 Predictor de Depósitos Bancarios")
st.markdown("""
Esta aplicación te permite predecir si un cliente realizará un depósito bancario
basado en diferentes características. Completa el formulario y obtén una predicción al instante.
""")

# URL del endpoint de predicción
API_URL = "http://127.0.0.1:8000/predict"

with st.sidebar:
    st.header("Acerca de")
    st.info("""
    Esta aplicación utiliza un modelo de machine learning entrenado 
    con datos bancarios para predecir la probabilidad de que un cliente 
    realice un depósito. La predicción se basa en características 
    personales y financieras del cliente.
    """)

    st.header("Instrucciones")
    st.markdown("""
    1. Completa todos los campos del formulario
    2. Haz clic en "Realizar Predicción"
    3. Observa el resultado y la explicación
    """)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Datos personales")
    age = st.slider("Edad", min_value=18, max_value=95, value=35)

    # Agregamos la opción de trabajo
    job_options = {
        0: "Administrativo",
        1: "Autónomo",
        2: "Desempleado",
        3: "Gerente",
        4: "Jubilado",
        5: "Obrero",
        6: "Otro",
        7: "Servicios",
        8: "Técnico"
    }
    job = st.selectbox(
        "Profesión",
        options=list(job_options.keys()),
        format_func=lambda x: job_options[x]
    )

    marital_options = {0: "Divorciado", 1: "Casado", 2: "Soltero"}
    marital = st.selectbox(
        "Estado civil",
        options=list(marital_options.keys()),
        format_func=lambda x: marital_options[x]
    )

    education_options = {0: "Primaria", 1: "Secundaria", 2: "Terciaria", 3: "Desconocido"}
    education = st.selectbox(
        "Educación",
        options=list(education_options.keys()),
        format_func=lambda x: education_options[x]
    )

    default_options = {0: "No", 1: "Sí"}
    default = st.selectbox(
        "¿Tiene crédito en incumplimiento?",
        options=list(default_options.keys()),
        format_func=lambda x: default_options[x]
    )

with col2:
    st.subheader("Datos financieros")
    balance = st.number_input("Saldo promedio", min_value=-10000, max_value=100000, value=2500)

    housing_options = {0: "No", 1: "Sí"}
    housing = st.selectbox(
        "¿Tiene préstamo hipotecario?",
        options=list(housing_options.keys()),
        format_func=lambda x: housing_options[x]
    )

    loan_options = {0: "No", 1: "Sí"}
    loan = st.selectbox(
        "¿Tiene préstamo personal?",
        options=list(loan_options.keys()),
        format_func=lambda x: loan_options[x]
    )

    # Añadimos tipo de contacto
    contact_options = {0: "Desconocido", 1: "Teléfono", 2: "Celular"}
    contact = st.selectbox(
        "Tipo de contacto",
        options=list(contact_options.keys()),
        format_func=lambda x: contact_options[x]
    )

with col3:
    st.subheader("Datos de contacto")
    month_options = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    month = st.selectbox(
        "Mes del último contacto",
        options=list(month_options.keys()),
        format_func=lambda x: month_options[x]
    )

    day = st.slider("Día del mes del último contacto", min_value=1, max_value=31, value=15)
    duration = st.slider("Duración del último contacto (segundos)", min_value=0, max_value=5000, value=180)
    campaign = st.slider("Número de contactos durante esta campaña", min_value=1, max_value=50, value=2)
    pdays = st.slider("Días desde el contacto anterior (-1 = nunca contactado)", min_value=-1, max_value=999, value=-1)
    previous = st.slider("Número de contactos previos a esta campaña", min_value=0, max_value=20, value=0)

    # Añadimos resultado de campaña anterior
    poutcome_options = {0: "Desconocido", 1: "Fracaso", 2: "Otro", 3: "Éxito"}
    poutcome = st.selectbox(
        "Resultado de la campaña anterior",
        options=list(poutcome_options.keys()),
        format_func=lambda x: poutcome_options[x]
    )

st.markdown("### Predicción")
prediccion_container = st.container()

if st.button("Realizar Predicción", type="primary"):
    with st.spinner("Realizando predicción..."):
        try:
            # Preparamos los parámetros en un diccionario
            params = {
                "age": age,
                "job": job,
                "marital": marital,
                "education": education,
                "default": default,
                "balance": balance,
                "housing": housing,
                "loan": loan,
                "contact": contact,
                "day": day,
                "month": month,
                "duration": duration,
                "campaign": campaign,
                "pdays": pdays,
                "previous": previous,
                "poutcome": poutcome
            }

            # Enviamos la solicitud usando query parameters
            response = requests.post(API_URL, params=params)

            if response.status_code == 200:
                result = response.json()

                with prediccion_container:
                    col_res1, col_res2 = st.columns([1, 2])

                    with col_res1:
                        if result["resultado"] == "Sí depositará":
                            st.success("POSITIVO: Sí realizará un depósito")
                            emoji = "✅"
                        else:
                            st.error("NEGATIVO: No realizará un depósito")
                            emoji = "❌"

                        st.markdown(f"## {emoji} {result['resultado']}")

                    with col_res2:
                        st.subheader("Factores importantes")
                        st.markdown("""
                        Los factores que más influyen en esta predicción son:
                        - **Duración del contacto**: Contactos más largos suelen indicar mayor interés
                        - **Saldo bancario**: Clientes con saldos más altos tienen mayor probabilidad de hacer depósitos
                        - **Edad**: Los rangos de edad medios suelen tener comportamientos más predecibles
                        """)

                st.subheader("Visualización de la predicción")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=100 if result["valor_prediccion"] == 1 else 0,
                    title={'text': "Probabilidad de depósito"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#1f77b4" if result["valor_prediccion"] == 1 else "#d62728"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccc"},
                            {'range': [50, 100], 'color': "#ccffcc"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Ver detalles de los datos utilizados"):
                    st.json(params)

            else:
                st.error(f"Error en la API: {response.text}")
                # Mostramos información detallada para ayudar a depurar
                st.write("Status code:", response.status_code)
                try:
                    st.write("Respuesta detallada:", response.json())
                except:
                    st.write("Texto de la respuesta:", response.text)

        except Exception as e:
            st.error(f"Error al conectar con la API: {str(e)}")
            st.info("Asegúrate de que la API esté funcionando en http://localhost:8000/predict")

st.markdown("---")
st.caption("Desarrollado con Streamlit y FastAPI para análisis predictivo bancario.")