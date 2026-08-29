import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 1: Load dataset
print("Loading dataset...")
df = pd.read_csv('TrafficTwoMonth.csv')

print("Columns in dataset:", df.columns.tolist())
print(df.head())

# Step 2: Encode 'Day of the week' if it's text (Monday, Tuesday, etc.)
if 'Day of the week' in df.columns:
    le_day = LabelEncoder()
    df['Day of the week'] = le_day.fit_transform(df['Day of the week'])
    joblib.dump(le_day, 'day_encoder.pkl')

# Step 3: Encode target variable (Traffic Situation: Heavy/High/Normal/Low)
le_target = LabelEncoder()
df['Traffic Situation'] = le_target.fit_transform(df['Traffic Situation'])
joblib.dump(le_target, 'target_encoder.pkl')

# Step 4: Select features and target
feature_cols = ['CarCount', 'BikeCount', 'BusCount', 'TruckCount', 'Total']
if 'Day of the week' in df.columns:
    feature_cols.append('Day of the week')

X = df[feature_cols]
y = df['Traffic Situation']

# Step 5: Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 7: Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))

# Step 8: Save trained model
joblib.dump(model, 'traffic_model.pkl')
print("\nModel saved as 'traffic_model.pkl'")