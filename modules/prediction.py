import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "students.csv"


def load_training_data():
    df = pd.read_csv(DATA_PATH)

    required = [
        "Department", "Semester", "Subject",
        "Marks", "Attendance"
    ]

    if not all(col in df.columns for col in required):
        raise ValueError("Required columns are missing from students.csv")

    return df.dropna(subset=required)


def predict_marks(department, semester, subject, attendance):

    df = load_training_data()

    features = ["Department", "Semester", "Subject", "Attendance"]
    target = "Marks"

    X = df[features].copy()
    y = df[target]

    categorical = ["Department", "Subject"]
    numerical = ["Semester", "Attendance"]

    preprocessing = ColumnTransformer([
        ("categorical",
         OneHotEncoder(handle_unknown="ignore"),
         categorical)
    ], remainder="passthrough")

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("regression", LinearRegression())
    ])

    model.fit(X, y)

    student = pd.DataFrame([{
        "Department": department,
        "Semester": semester,
        "Subject": subject,
        "Attendance": attendance
    }])

    prediction = model.predict(student)[0]

    return round(max(0, min(100, prediction)), 2)
def load_training_data(df=None):
    if df is not None and not df.empty:
        return df.copy()
    return pd.read_csv(DATA_PATH)
def evaluate_model(df=None):


    df = load_training_data(df)

    features = ["Department", "Semester", "Subject", "Attendance"]
    target = "Marks"

    X = df[features]
    y = df[target]

    if len(df) < 8:
        raise ValueError("At least 8 student records are required for model evaluation.")

    categorical = ["Department", "Subject"]
    numerical = ["Semester", "Attendance"]

    preprocessing = ColumnTransformer([
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical
        )
    ], remainder="passthrough")

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("regression", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    predictions = [round(max(0, min(100, float(p))), 2) for p in predictions]

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    comparison_df = pd.DataFrame(
        {
            "Actual Marks": list(y_test),
            "Predicted Marks": predictions,
        }
    )

    return {
        "MAE": round(float(mae), 2),
        "RMSE": round(float(rmse), 2),
        "R2 Score": round(float(r2), 4),
        "Training Records": len(X_train),
        "Testing Records": len(X_test),
        "Comparison": comparison_df,
        
    }