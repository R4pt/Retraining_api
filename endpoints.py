from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import uvicorn

app = FastAPI(title="API de Predicción de Depósitos")

model = joblib.load("best_logistic_model.joblib")

@app.post("/predict")
def predict(
        age: int,
        balance: float,
        day: int,
        duration: int,
        campaign: int,
        pdays: int,
        previous: int,
        housing: int,
        loan: int,
        marital: int,
        education: int,
        default: int,
        month: int,

):
    try:
        input_data = {
            "age": [age],
            "marital": [marital],
            "education": [education],
            "default": [default],
            "balance": [balance],
            "housing": [housing],
            "loan": [loan],
            "day": [day],
            "month": [month],
            "duration": [duration],
            "campaign": [campaign],
            "pdays": [pdays],
            "previous": [previous]
        }

        feature_order = [
            "age", "marital", "education", "default", "balance",
            "housing", "loan", "day", "month", "duration",
            "campaign", "pdays", "previous"
        ]

        df = pd.DataFrame(input_data)
        df = df[feature_order]

        prediction = model.predict(df)[0]

        result = "Sí depositará" if prediction == 1 else "No depositará"

        return {
            "resultado": result,
            "valor_prediccion": int(prediction)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al realizar la predicción: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "endpoints:app",
        port=8000,
        reload=True
    )
