import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load dataset
df = pd.read_csv("sign_language_cleaned.csv")

# Encode gesture labels
le = LabelEncoder()
df["gesture"] = le.fit_transform(df["gesture"])

# Split features and labels
X = df.drop(columns=["gesture"])
y = df["gesture"]

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
feature_importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

# Plot feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x="Importance", y="Feature", data=feature_importance_df[:20], palette="viridis")
plt.title("Top 20 Feature Importances (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()

# Save the important features
top_features = feature_importance_df["Feature"].values[:20]
X_selected = X[top_features]

# Save the refined dataset
refined_df = pd.concat([X_selected, y], axis=1)
refined_df.to_csv("sign_language_refined.csv", index=False)

print("Feature importance analysis complete. Refined dataset saved as 'sign_language_refined.csv'.")
