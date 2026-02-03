import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load dataset
df = pd.read_csv("balanced_environmental_data.csv")

# 2. Encode labels
le = LabelEncoder()
df['disease_label'] = le.fit_transform(df['Predicted_Disease'])

# 3. Features and labels
X = df[['temperature', 'humidity']]
y = df['disease_label']

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- RANDOM FOREST ---
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

print("🌲 Random Forest Results")
print("Accuracy:", accuracy_score(y_test, rf_preds))
print(classification_report(y_test, rf_preds, target_names=le.classes_))

# Save model
joblib.dump(rf_model, "random_forest_disease_model.pkl")

# Plot feature importance
rf_importances = rf_model.feature_importances_
sns.barplot(x=X.columns, y=rf_importances)
plt.title("Random Forest Feature Importance")
plt.ylabel("Importance Score")
plt.show()

# --- XGBOOST ---
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)

print("\n⚡ XGBoost Results")
print("Accuracy:", accuracy_score(y_test, xgb_preds))
print(classification_report(y_test, xgb_preds, target_names=le.classes_))

# Save model
joblib.dump(xgb_model, "xgboost_disease_model.pkl")

# Plot XGBoost feature importance
xgb_importances = xgb_model.feature_importances_
sns.barplot(x=X.columns, y=xgb_importances)
plt.title("XGBoost Feature Importance")
plt.ylabel("Importance Score")
plt.show()
