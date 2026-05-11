import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import joblib
import os

print("Loading data...")

data = pd.read_csv("data/train_transaction.csv")

print("Engineering features...")

data['hour'] = (data['TransactionDT'] // 3600) % 24
data['day'] = (data['TransactionDT'] // (3600 * 24)) % 7

Y = data['isFraud']

data = data.drop(columns=['TransactionID', 'isFraud', 'TransactionDT'])

null = data.isnull().sum()
good_cols = null[null < 120000].index.tolist()
X = data[good_cols]
X = X.copy()

numeric_cols = X.select_dtypes(exclude='object').columns
X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].median())

cat_cols = X.select_dtypes(include='object').columns
X[cat_cols] = X[cat_cols].fillna('missing')
X = pd.get_dummies(X, columns=cat_cols)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.17, random_state=42, stratify=Y)

print("Training Random Forest...")

model_Random_Forest = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
model_Random_Forest.fit(X_train, y_train)

y_pred = model_Random_Forest.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))

joblib.dump(model_Random_Forest, 'models/random_forest.pkl')

print("Random Forest saved")

print("Training XGBoost...")

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model_xgb = XGBClassifier(
    n_estimators=100,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1,
    eval_metric='aucpr'
)
model_xgb.fit(X_train, y_train)
y_pred_xgb = model_xgb.predict(X_test)
print(classification_report(y_test, y_pred_xgb, target_names=['Legitimate', 'Fraud']))

joblib.dump(model_xgb, 'models/xgboost.pkl')
print("XGBoost saved")
