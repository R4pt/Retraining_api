import polars as pl
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import joblib

file_path = 'bank.csv'
df = pl.read_csv(file_path)

df_cleaned = df.drop_nulls()

df_cleaned = df_cleaned.with_columns(
    (pl.when(pl.col("housing") == "no").then(0).otherwise(1).cast(pl.Int8()).alias("housing")),
    (pl.when(pl.col("loan") == "no").then(0).otherwise(1).cast(pl.Int8()).alias("loan")),
    (pl.when(pl.col("marital") == "divorced").then(0).otherwise(1).cast(pl.Int8()).alias("marital")),
    (pl.when(pl.col("education") == "secondary").then(0).otherwise(1).cast(pl.Int8()).alias("education")),
    (pl.col("default").map_elements(lambda x: False if x.lower() == "no" else True, return_dtype=pl.Boolean)).cast(pl.Int8()).alias("default"),
    (pl.col("deposit").map_elements(lambda x: False if x.lower() == "no" else True, return_dtype=pl.Boolean)).cast(pl.Int8()).alias("deposit"),
    pl.when(pl.col("month") == "jan").then(1).when(pl.col("month") == "feb").then(2).when(pl.col("month") == "mar").then(3).when(pl.col("month") == "apr").then(4).when(pl.col("month") == "may").then(5)
      .when(pl.col("month") == "jun").then(6).when(pl.col("month") == "jul").then(7).when(pl.col("month") == "aug").then(8).when(pl.col("month") == "sep").then(9)
      .when(pl.col("month") == "oct").then(10).when(pl.col("month") == "nov").then(11).when(pl.col("month") == "dec").then(12).cast(pl.Int8()).alias("month")
)

df_cleaned = df_cleaned.drop(["contact","poutcome", "job"])

unnamed_columns = [col for col in df_cleaned.columns if col == ""]
if unnamed_columns:
    df_cleaned = df_cleaned.drop(unnamed_columns)


X = df_cleaned.drop(['deposit'])
y = df_cleaned['deposit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression(max_iter=1000))
])

param_grid = {
    "logistic__C": [0.1, 1, 10, 100],
    "logistic__solver": ["liblinear", "lbfgs"]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="accuracy")
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

coefficients = best_model.named_steps["logistic"].coef_[0]
features_names = X_train.columns

plt.figure(figsize=(10, 6))
plt.barh(features_names, coefficients, color="skyblue")
plt.xlabel('Coeficiente')
plt.title('Importancia de las características en el modelo de regresión logística')
plt.savefig("feature_importance.png", dpi=120)
plt.close()

y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

with open("metrics.txt", "w") as outfile:
    outfile.write(f"Training Accuracy: {accuracy}")

model_path = "best_logistic_model.joblib"
joblib.dump(best_model, model_path)
