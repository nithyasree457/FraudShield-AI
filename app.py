from flask import Flask, render_template, request, send_file
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load model
model = pickle.load(open("model/fraud_model.pkl", "rb"))

# Load original dataset
data = pd.read_csv("dataset/creditcard.csv")

required_columns = list(data.drop("Class", axis=1).columns)


@app.route("/")
def home():

    return render_template(
        "index.html",
        total_transactions=len(data),
        fraud_cases=len(data[data["Class"] == 1]),
        roc_auc=0.975
    )


@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:
            return render_template(
                "index.html",
                total_transactions=len(data),
                fraud_cases=len(data[data["Class"] == 1]),
                error="No file selected."
            )

        file = request.files["file"]

        if file.filename == "":
            return render_template(
                "index.html",
                total_transactions=len(data),
                fraud_cases=len(data[data["Class"] == 1]),
                error="Please select a CSV file."
            )

        # Read uploaded file
        df = pd.read_csv(file)

        # Validate columns
        if list(df.columns) != required_columns:

            return render_template(
                "index.html",
                total_transactions=len(data),
                fraud_cases=len(data[data["Class"] == 1]),
                error="Invalid dataset format. CSV must contain Time, V1-V28 and Amount columns."
            )

        # Predict
        predictions = model.predict(df)

        fraud_count = int(sum(predictions))
        total_records = len(predictions)

        fraud_percent = round(
            (fraud_count / total_records) * 100,
            2
        )

        # Risk Level
        if fraud_percent < 5:
            risk = "🟢 LOW"
        elif fraud_percent < 20:
            risk = "🟠 MEDIUM"
        else:
            risk = "🔴 HIGH"

        # Save result file
        result_df = df.copy()

        result_df["Prediction"] = [
            "Fraud" if p == 1 else "Normal"
            for p in predictions
        ]

        result_df.to_csv(
            "fraud_results.csv",
            index=False
        )

        analysis = {
            "total": total_records,
            "fraud": fraud_count,
            "normal": total_records - fraud_count,
            "percent": fraud_percent,
            "risk": risk,
            "filename": file.filename,
            "columns": len(df.columns)
        }

        return render_template(
            "index.html",
            total_transactions=len(data),
            fraud_cases=len(data[data["Class"] == 1]),
            roc_auc=0.975,
            analysis=analysis
        )

    except Exception as e:

        return render_template(
            "index.html",
            total_transactions=len(data),
            fraud_cases=len(data[data["Class"] == 1]),
            roc_auc=0.975,
            error=str(e)
        )


@app.route("/download")
def download():

    if os.path.exists("fraud_results.csv"):

        return send_file(
            "fraud_results.csv",
            as_attachment=True
        )

    return "No report generated yet."


if __name__ == "__main__":
    app.run(debug=True)