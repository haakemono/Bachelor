import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("sign_langauge_data.csv", dtype={col: float for col in df.columns[1:]}, low_memory=False)

# Remove incorrect row with "gesture" as value
df = df[df["gesture"] != "gesture"]

# Convert all feature columns to numeric (force non-numeric to NaN)
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

# Drop rows with NaN values
df.dropna(inplace=True)

# Print the count of each gesture in the dataset
gesture_counts = df["gesture"].value_counts()
print("\n Gesture Data Count:")
print(gesture_counts)

# Separate features (X) and labels (y)
X = df.drop(columns=["gesture"])  # Features
y = df["gesture"]  # Labels

# Convert labels to numerical values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Save label encoder for later use in recognition
joblib.dump(label_encoder, "label_encoder.pkl")

# Convert features to `float32`
X = X.astype(np.float32)

# Convert DataFrame to NumPy array before training
X = X.to_numpy()

# Split into training and test sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Ensure all values are numeric before training
if not np.isfinite(X_train).all():
    print("\n Debug: X_train contains non-numeric values! Showing first 5 rows:")
    print(X_train[:5])
    print("\n Exiting program. Please check `gesture_data.csv` for bad data.")
    exit()

# Compute class weights to handle imbalance
from sklearn.utils.class_weight import compute_class_weight
class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y), y=y)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Define the neural network model
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.4),  # Prevent overfitting
    keras.layers.Dense(64, activation='relu', kernel_regularizer=keras.regularizers.l2(0.01)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.4),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(len(np.unique(y)), activation='softmax')  # Output layer
])

# Implement learning rate scheduling
lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=0.01, decay_steps=1000, decay_rate=0.9
)
optimizer = keras.optimizers.Adam(learning_rate=lr_schedule)

# Compile the model
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model with validation split
print("\n Training Neural Network...")
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test), class_weight=class_weight_dict)

# Evaluate accuracy
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\n Model Accuracy on Test Data: {test_acc:.2f}")

# Save the model in **native Keras format**
model.save("sign_langauge_data.keras", save_format="keras")

print(" Model and label encoder saved successfully.")