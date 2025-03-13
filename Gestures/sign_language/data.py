import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load dataset
df = pd.read_csv("sign_langauge_data.csv")

# Encode gesture labels
le = LabelEncoder()
df["gesture"] = le.fit_transform(df["gesture"])

# Split features and labels
X = df.drop(columns=["gesture"])
y = df["gesture"]

# Convert all features to numeric, coerce errors into NaN
for col in X.columns:
    X[col] = pd.to_numeric(X[col], errors='coerce')

# Drop any rows with NaN values
X = X.dropna()
y = y.loc[X.index]  # Align y with cleaned X

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a RandomForestClassifier to get feature importance
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_scaled, y)

# Get feature importance
importances = rf.feature_importances_
feature_names = X.columns

# Create a DataFrame for visualization
feature_importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x="Importance", y="Feature", data=feature_importance_df[:20], palette="viridis")
plt.title("Top 20 Feature Importances (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# Save the top 20 features
top_features = feature_importance_df["Feature"].values[:20]
X_selected = X[top_features]

# Save refined dataset
refined_df = pd.concat([X_selected, y], axis=1)
refined_df.to_csv("sign_language_refined.csv", index=False)

print("Feature importance analysis complete. Refined dataset saved as 'sign_language_refined.csv'.")


from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=y, palette="tab10")
plt.title("PCA: Gesture Clusters in 2D Space")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend(title="Gesture")
plt.show()



from sklearn.metrics import classification_report, confusion_matrix

y_pred = rf.predict(X_scaled)
print(classification_report(y, y_pred))
sns.heatmap(confusion_matrix(y, y_pred), annot=True)


from scipy.spatial.distance import cdist

gesture_means = X.groupby(y).mean()
dist_matrix = cdist(gesture_means, gesture_means)
sns.heatmap(dist_matrix, annot=True)


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
sns.countplot(x=y)
plt.title("Distribution of Gesture Classes")
plt.xlabel("Gesture Class")
plt.ylabel("Count")
plt.show()


from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=y, palette="tab20", legend=False)
plt.title("PCA Projection of Gestures (2D)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.show()


from sklearn.metrics import confusion_matrix
import seaborn as sns

y_pred = rf.predict(X_scaled)
cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(12,10))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix of Gesture Classification")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# One-hot encode labels
y_encoded = to_categorical(y)

# Train/test split
X_train, X_val, y_train, y_val = train_test_split(X_selected, y_encoded, test_size=0.2, random_state=42)

# Build the model
model = Sequential()
model.add(Dense(128, input_shape=(X_selected.shape[1],), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(25, activation='softmax'))  # 25 classes

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_val, y_val), batch_size=32)

# Evaluate
loss, accuracy = model.evaluate(X_val, y_val)
print(f"Validation Accuracy: {accuracy:.2f}")
