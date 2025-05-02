from fastapi import FastAPI, HTTPException
import joblib
import polars as pl
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
        month: int
):
    try:
        data = {
            "age": age,
            "balance": balance,
            "day": day,
            "duration": duration,
            "campaign": campaign,
            "pdays": pdays,
            "previous": previous,
            "housing": housing,
            "loan": loan,
            "marital": marital,
            "education": education,
            "default": default,
            "month": month
        }

        df = pl.DataFrame([data])

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
        host="0.0.0.0",
        port=8000
    )