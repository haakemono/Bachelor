import pandas as pd
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

# Load dataset
file_path = "sign_langauge_data.csv"
df = pd.read_csv(file_path)

# Convert numerical columns to float
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return np.nan

for col in df.columns[1:]:  
    df[col] = df[col].apply(convert_to_float)

# Drop rows with NaN values
df.dropna(inplace=True)

# Extract features and labels
X = df.iloc[:, 1:].values  
y = df.iloc[:, 0].values   

# Encode gesture labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define neural network model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
    keras.layers.Dropout(0.3),  
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(len(np.unique(y)), activation='softmax')
])


# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Evaluate model
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc * 100:.2f}%")

# Save model
model.save("gesture_recognition_model.h5")

# Save label encoder

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Save Scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
