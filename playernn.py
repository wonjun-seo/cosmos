import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import numpy as np

class PlayerRatingLSTM(nn.Module):
    """
    LSTM-based regressor for predicting team goals.
    Input shape: (batch_size, seq_len=1, input_size)
    Output: (batch_size, 1)
    """
    def __init__(self, input_size, hidden_size=128, num_layers=2, dropout=0.2):
        super(PlayerRatingLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (batch, seq_len, input_size)
        out, _ = self.lstm(x)                 # out: (batch, seq_len, hidden_size)
        last_out = out[:, -1, :]              # take output at last time step
        return self.fc(last_out)              # (batch, 1)


if __name__ == "__main__":
    # ---------------------------
    # Training script
    # ---------------------------
    # Assumes you have a file 'player_data.pkl' with dict keys:
    #   'X_train': numpy array (n_samples, n_features)
    #   'y_train': numpy array (n_samples,)
    # Optionally, 'X_val', 'y_val' for validation.
    
    # Hyperparameters
    EPOCHS = 50
    BATCH_SIZE = 32
    LEARNING_RATE = 1e-3
    MODEL_PATH = 'player_nn_model_weights.pth'
    DATA_PATH = 'player_model_and_data.pkl'

    # Device setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load training (and optional validation) data
    with open(DATA_PATH, 'rb') as f:
        data = pickle.load(f)
    X_train = data['X_train']      # shape: (n_train, n_features)
    y_train = data['y_train']      # shape: (n_train,)
    X_val = data.get('X_val', None)
    y_val = data.get('y_val', None)

    # Convert to torch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32).unsqueeze(1).to(device)
    y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1).to(device)
    if X_val is not None:
        X_val = torch.tensor(X_val, dtype=torch.float32).unsqueeze(1).to(device)
        y_val = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1).to(device)

    # Initialize model
    input_size = X_train.shape[2]
    model = PlayerRatingLSTM(input_size=input_size).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_loss = float('inf')
    best_state = None

    # Training loop
    for epoch in range(1, EPOCHS + 1):
        model.train()
        perm = torch.randperm(X_train.size(0))
        train_loss = 0.0
        for i in range(0, len(perm), BATCH_SIZE):
            idx = perm[i:i + BATCH_SIZE]
            batch_X = X_train[idx]
            batch_y = y_train[idx]

            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * batch_X.size(0)

        train_loss /= X_train.size(0)

        # Validation
        if X_val is not None:
            model.eval()
            with torch.no_grad():
                val_out = model(X_val)
                val_loss = criterion(val_out, y_val).item()
        else:
            val_loss = train_loss

        print(f"Epoch {epoch}/{EPOCHS} - train loss: {train_loss:.4f} - val loss: {val_loss:.4f}")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = model.state_dict()

    # Write out best model weights
    if best_state is not None:
        torch.save(best_state, MODEL_PATH)
        print(f"Best model saved with val loss: {best_val_loss:.4f}")
    else:
        torch.save(model.state_dict(), MODEL_PATH)
        print("Model saved (no validation split provided)")

    # Ensure training features are saved for scaler building
    # Overwrites player_data.pkl to contain only X_train for scaler
    with open('player_data.pkl', 'wb') as f:
        pickle.dump({'X_train': data['X_train']}, f)
        print("Saved X_train for scaler in 'player_data.pkl'.")

#lines below are old code




















'''import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle 
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

sns.set(style='whitegrid')

np.random.seed(42)



torch.manual_seed(87) 
player_original_df = pd.read_csv('player_attributes_cleaned.csv')
player_cleaned_df = player_original_df.drop(columns="date")


# Define which columns to use as input features
feature_cols = [col for col in player_cleaned_df.columns if col not in ['overall_rating', 'player_api_id']]
sequence_length = 3

X_list = []
y_list = []

# Group data by player
for _, group in player_cleaned_df.groupby('player_api_id'):
    group = group.reset_index(drop=True)
    if len(group) <= sequence_length:
        continue

    for i in range(len(group) - sequence_length):
        X_seq = group.loc[i:i+sequence_length-1, feature_cols].to_numpy(dtype=np.float32)
        y_val = group.loc[i + sequence_length, 'overall_rating']  # <== here's the `y_val` you mentioned
        X_list.append(X_seq)
        y_list.append(y_val)

# Convert to PyTorch tensors
X_tensor = torch.tensor(np.stack(X_list))           # Shape: (samples, seq_len, features)
y_tensor = torch.tensor(y_list, dtype=torch.float32).unsqueeze(1)  # Shape: (samples, 1)

import torch.nn as nn

class PlayerRatingLSTM(nn.Module):
    def __init__(self, input_size=13, hidden_size=128, num_layers=1, output_size=1):
        super(PlayerRatingLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out

class PlayerRatingLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        out, _ = self.lstm(x)  # out: (batch, seq_len, hidden_size)
        last_output = out[:, -1, :]  # Take the last time step
        return self.fc(last_output)

class CustomLoss(nn.Module):
    def __init__(self):
        super(CustomLoss, self).__init__()

    def forward(self, predictions, targets):
        return torch.mean((predictions - targets)[3:] ** 2)
    


# Train/val split
train_ratio = 0.8
n_total = X_tensor.shape[0]
n_train = int(n_total * train_ratio)

X_train, X_val = X_tensor[:n_train], X_tensor[n_train:]
y_train, y_val = y_tensor[:n_train], y_tensor[n_train:]

train_ds = TensorDataset(X_train, y_train)
val_ds = TensorDataset(X_val, y_val)

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=64)

# Model setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PlayerRatingLSTM(input_size=X_tensor.shape[2]).to(device)
loss_fn = CustomLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# History
train_losses = []
val_losses = []

# Best model
best_val_loss = float('inf')     # starting with infinity
best_model_state = None          # best model parameters

mae_loss = nn.L1Loss()

# Train loop
n_epochs = 30
for epoch in range(n_epochs):
    model.train()
    train_loss = 0.0
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        pred = model(xb)
        loss = loss_fn(pred, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            val_loss += loss_fn(model(xb), yb).item()
            
    avg_train_loss = train_loss / len(train_loader)
    avg_val_loss = val_loss / len(val_loader)
    train_losses.append(avg_train_loss)
    val_losses.append(avg_val_loss)

    # Save best model
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        best_model_state = model.state_dict()
            
    print(f"Epoch {epoch+1}/{n_epochs}, Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss/len(val_loader):.4f}")

print("Training completed!")

model.load_state_dict(best_model_state)        # Recover the best model
print(f"Best loss: {best_val_loss:.4f}")

import random
i = random.randint(0, X_tensor.shape[0] - 1)  # change this to test different examples

# Move input and true label to device
sample_input = X_tensor[i:i+1].to(device)     # Shape: (1, seq_len, features)
actual_rating = y_tensor[i].item()            # Scalar

# Get prediction
model.eval()
with torch.no_grad():
    predicted_rating = model(sample_input).item()

print(f"Predicted Rating: {predicted_rating:.2f}")
print(f"Actual Rating:    {actual_rating:.2f}")

from torch.nn import L1Loss

# Randomly sample 1000 points from the dataset
sample_indices = torch.randperm(len(X_tensor))[:1000]
X_sample = X_tensor[sample_indices].to(device)
y_sample = y_tensor[sample_indices].to(device)

model.eval()
with torch.no_grad():
    preds = model(X_sample)

mae = L1Loss(reduction='none')
losses = mae(preds, y_sample).cpu().numpy()

plt.figure(figsize=(8, 5))  
plt.hist(losses, bins=40, color='skyblue', edgecolor='black')
plt.xlabel("Mean Absolute Error")
plt.ylabel("Frequency")
plt.title("Distribution of MAE over 1000 Sampled Predictions")
plt.grid(True)
#plt.show()


import ipywidgets as widgets
from IPython.display import display, clear_output

# Choose a player_api_id to visualize
player_id = player_cleaned_df['player_api_id'].iloc[0]  # You can change this to any valid player_api_id

# Get all rows for this player
player_df = player_cleaned_df[player_cleaned_df['player_api_id'] == player_id].reset_index(drop=True)

# Prepare input sequences for this player (skip first 'sequence_length' entries)
X_player = []
for i in range(len(player_df) - sequence_length):
    X_seq = player_df.loc[i:i+sequence_length-1, feature_cols].to_numpy(dtype=np.float32)
    X_player.append(X_seq)
X_player_tensor = torch.tensor(np.stack(X_player)).to(device)

# Predict ratings
model.eval()
with torch.no_grad():
    preds = model(X_player_tensor).cpu().numpy().flatten()

# Actual ratings (skip first 'sequence_length' entries to align with predictions)
actual_ratings = player_df['overall_rating'].iloc[sequence_length:].to_numpy()

def MSE(actual_ratings, preds):
    return np.mean((actual_ratings - preds) ** 2)

def plot_player(player_id):
    player_df = player_original_df[player_original_df['player_api_id'] == player_id].reset_index(drop=True)
    player_name = player_df.iloc[0]['player_name']
    X_player = []
    for i in range(len(player_df) - sequence_length):
        X_seq = player_df.loc[i:i+sequence_length-1, feature_cols].to_numpy(dtype=np.float32)
        X_player.append(X_seq)
    if len(X_player) == 0:
        print(f"Player {player_id} does not have enough records.")
        return
    X_player_tensor = torch.tensor(np.stack(X_player)).to(device)
    model.eval()
    with torch.no_grad():
        preds = model(X_player_tensor).cpu().numpy().flatten()
    # Actual ratings
    #  (skip first 'sequence_length' entries to align with predictions)
    actual_ratings = player_df['overall_rating'].iloc[sequence_length:].to_numpy()
    ages = player_df['age'].iloc[sequence_length:].to_numpy()
    mse = MSE(actual_ratings, preds)
    y_min = min(actual_ratings.min(), preds.min())
    y_max = max(actual_ratings.max(), preds.max())
    if y_max - y_min < 18:
        center = (y_min + y_max) / 2
        y_lower = center - 7.5
        y_upper = center + 7.5
    else:
        y_lower = y_min
        y_upper = y_max
    plt.figure(figsize=(10, 5))
    plt.plot(ages, actual_ratings, label='Actual Rating', marker='o')
    plt.plot(ages, preds, label='Predicted Rating', marker='x')
    for age, actual, pred in zip(ages, actual_ratings, preds):
        plt.plot([age, age], [actual, pred], color='gray', linestyle='--', linewidth=0.7)

    plt.xlabel('Age')
    plt.ylabel('Overall Rating')
    plt.title(f'{player_name} - Actual vs Predicted Ratings\nPlayer ID: {player_id} \nMSE: {mse:.2f}')

    plt.legend()
    plt.ylim(y_lower -3, y_upper+3)
    #plt.show()

button = widgets.Button(description="Random Player")
output = widgets.Output()

def on_button_clicked(b):
    with output:
        clear_output(wait=True)
        random_id = np.random.choice(player_cleaned_df['player_api_id'].unique())
        plot_player(random_id)

button.on_click(on_button_clicked)
display(button, output)


save_dict = {
    'model_class': PlayerRatingLSTM,             # So you can reinstantiate model if needed
    'model_state_dict': model.state_dict(),      # Trained weights
    'input_size': X_tensor.shape[2],             # Input size for reconstruction
    'X_tensor': X_tensor,                        # Input data
    'y_tensor': y_tensor,                        # Labels
    'feature_cols': feature_cols,                # Feature names
    'sequence_length': sequence_length,          # For reproducibility
    'player_cleaned_df': player_cleaned_df,      # Optionally the cleaned DataFrame
    'best_val_loss': best_val_loss               # Track performance
}

with open('player_model_and_data.pkl', 'wb') as f:
    pickle.dump(save_dict, f)




torch.save(model, "model.pkl")
torch.save(model.state_dict(), 'player_nn_model_weights.pth')



with open('player_nn_model.pkl', 'wb') as f:
    pickle.dump(model, f)

'''