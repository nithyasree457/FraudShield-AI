import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from imblearn.over_sampling import SMOTE

# LOAD DATA
data = pd.read_csv("dataset/creditcard.csv")

# FEATURES & TARGET
X = data.drop("Class", axis=1)
y = data["Class"]

# SCALE AMOUNT & TIME
scaler = StandardScaler()

X["Amount"] = scaler.fit_transform(X[["Amount"]])
X["Time"] = scaler.fit_transform(X[["Time"]])

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# HANDLE IMBALANCE
smote = SMOTE(random_state=42)

X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train,
    y_train
)

# MODEL
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_resampled, y_train_resampled)

# PREDICTIONS
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]

print("\nClassification Report\n")
print(classification_report(y_test, y_pred))

print("\nROC AUC Score")
print(roc_auc_score(y_test, y_prob))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

# SAVE MODEL
with open("model/fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel Saved Successfully")