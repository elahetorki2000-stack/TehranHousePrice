import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

print("="*50)
print("Starting data preprocessing and model training...")
print("="*50)

# 1. Load dataset
if not os.path.exists('housePrice.csv'):
    print("[❌] Error: housePrice.csv not found in the current directory!")
    exit()

df = pd.read_csv('housePrice.csv')
print(f"[✔] Dataset loaded successfully. Total rows: {len(df)}")

# 2. Data preprocessing and cleaning
df.dropna(subset=['Area', 'Room', 'Price', 'Address'], inplace=True)

# Convert Area to float after removing commas
df['Area'] = df['Area'].astype(str).str.replace(',', '').astype(float)

# Convert boolean-like features to binary integers (0 or 1)
for col in ['Parking', 'Warehouse', 'Elevator']:
    df[col] = df[col].astype(bool).astype(int)

# Encode categorical Address column to numerical codes
df['Address_code'] = df['Address'].astype('category').cat.codes

# Save address mapping for future web service prediction
address_mapping = dict(zip(df['Address'], df['Address_code']))
joblib.dump(address_mapping, 'address_mapping.pkl')

# 3. Define features (X) and target variable (y)
X = df[['Area', 'Room', 'Parking', 'Warehouse', 'Elevator', 'Address_code']]
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and train Random Forest Regressor
print("[...] Training the model (this might take a few seconds)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate model performance using standard metrics (R2, MAE, RMSE)
y_pred = model.predict(X_test)
r2_score = model.score(X_test, y_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"[✔] Model trained successfully.")
print(f"    - R2 Score (Accuracy): {r2_score:.2%}")
print(f"    - Mean Absolute Error (MAE): {mae:,.2f} IRR")
print(f"    - Root Mean Squared Error (RMSE): {rmse:,.2f} IRR")

# 6. Serialize and save the trained model
joblib.dump(model, 'housing_model.pkl')
print("[✔] Model saved successfully as 'housing_model.pkl'")
print("="*50)