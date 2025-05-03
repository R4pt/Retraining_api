# Predictor de Depósitos Bancarios

Este proyecto implementa un modelo de inteligencia artificial para predecir si un cliente realizará un depósito bancario basado en características personales y financieras.

## Descripción

El sistema utiliza un modelo de regresión logística entrenado con datos bancarios históricos para predecir la probabilidad de que un cliente realice un depósito. El proyecto incluye:

- Un modelo de machine learning entrenado con datos bancarios
- Una API REST para realizar predicciones
- Una interfaz gráfica web interactiva para usuarios finales

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clone este repositorio:
   ```
   git clone <url-del-repositorio>
   ```

2. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Estructura del proyecto

- `bank.csv`: Datos de entrenamiento del modelo
- `requirements.txt`: Dependencias del proyecto
- `retraining.py`: Script para entrenar/reentrenar el modelo
- `endpoints.py`: API de predicción (FastAPI)
- `interfaz.py`: Interfaz gráfica de usuario (Streamlit)
- `metrics.txt`: Métricas de rendimiento del modelo
- `feature_importance.png`: Visualización de la importancia de las características
- `best_logistic_model.joblib`: Modelo entrenado guardado

## Entrenamiento del modelo

Para entrenar o reentrenar el modelo con nuevos datos:

1. Asegúrese de que el archivo `bank.csv` está presente y contiene los datos correctos
2. Ejecute el script de entrenamiento:
   ```
   python retraining.py
   ```

Este script:
- Carga y limpia los datos
- Entrena un modelo de regresión logística con optimización de hiperparámetros
- Guarda el modelo entrenado como `best_logistic_model.joblib`
- Genera un archivo de métricas (`metrics.txt`) y una visualización de importancia de características (`feature_importance.png`)

## Ejecución de la API

Para iniciar el servidor de la API:

1. Asegúrese de que el archivo `best_logistic_model.joblib` existe
2. Ejecute:
   ```
   python endpoints.py
   ```

La API estará disponible en `http://localhost:8000`

### Endpoints de la API

- **POST /predict**: Realiza una predicción basada en los datos proporcionados
  - Parámetros de entrada: Características del cliente como edad, estado civil, balance, etc.
  - Resultado: Predicción sobre si el cliente realizará un depósito

## Interfaz gráfica

Para iniciar la interfaz de usuario:

1. Asegúrese de que la API está en ejecución
2. Ejecute:
   ```
   streamlit run interfaz.py
   ```

La interfaz estará disponible en `http://localhost:8501`

### Uso de la interfaz

1. Complete el formulario con los datos del cliente
2. Haga clic en "Realizar Predicción"
3. Visualice los resultados y la explicación de la predicción

## Inputs y Outputs del modelo

### Inputs
- **age**: Edad del cliente (entero)
- **marital**: Estado civil (0: Divorciado, 1: Casado, 2: Soltero)
- **education**: Nivel educativo (0: Primaria, 1: Secundaria, 2: Terciaria, 3: Desconocido)
- **default**: Si tiene crédito en incumplimiento (0: No, 1: Sí)
- **balance**: Saldo promedio en cuenta (número decimal)
- **housing**: Si tiene préstamo hipotecario (0: No, 1: Sí)
- **loan**: Si tiene préstamo personal (0: No, 1: Sí)
- **day**: Día del mes del último contacto (1-31)
- **month**: Mes del último contacto (1-12)
- **duration**: Duración del último contacto en segundos (entero)
- **campaign**: Número de contactos realizados durante esta campaña (entero)
- **pdays**: Días transcurridos desde el contacto previo (-1 si no fue contactado)
- **previous**: Número de contactos previos antes de esta campaña (entero)

### Outputs
- **resultado**: Texto que indica "Sí depositará" o "No depositará"
- **valor_prediccion**: Valor numérico de la predicción (1: Sí depositará, 0: No depositará)

## Arquitectura del sistema

El proyecto sigue una arquitectura de tres capas:

1. **Capa de modelo**: Modelo entrenado con scikit-learn (regresión logística)
2. **Capa de API**: Implementada con FastAPI, proporciona endpoints para realizar predicciones
3. **Capa de presentación**: Interfaz gráfica implementada con Streamlit

## Mantenimiento

Para mantener el modelo actualizado:

1. Actualice el archivo `bank.csv` con nuevos datos
2. Ejecute `python retraining.py` para reentrenar el modelo
3. Reinicie la API para que utilice el nuevo modelo entrenado


