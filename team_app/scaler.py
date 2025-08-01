# build_scaler.py

import pickle
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# 1) Load the same data bundle you use in your Flask app:
with open("player_model_and_data.pkl", "rb") as f:
    data = pickle.load(f)

# 2) Extract X_tensor and convert to NumPy 2D array of shape (n_samples, n_features):
X_tensor = data["X_tensor"]  # torch.Tensor or something similar
# If it's a PyTorch tensor:
try:
    X_np = X_tensor.squeeze(1).numpy()
except AttributeError:
    # If X_tensor is a list of tensors:
    import torch
    X_np = torch.stack(X_tensor).squeeze(1).numpy()

# 3) Fit and dump the scaler:
scaler = StandardScaler().fit(X_np)
joblib.dump(scaler, "scaler.pkl")

print(f"Fitted scaler on data with shape {X_np.shape} → saved scaler.pkl")
