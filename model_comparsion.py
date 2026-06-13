import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("dataset/creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

scaler = StandardScaler()

X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
   "Logistic Regression": LogisticRegression(max_iter=3000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42)
}

scores = []

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    score = f1_score(y_test, pred)

    scores.append(score)

plt.figure(figsize=(8,5))
plt.bar(models.keys(), scores)

plt.title("Model Comparison (F1 Score)")
plt.ylabel("F1 Score")

plt.savefig("static/model_comparison.png")

plt.show()