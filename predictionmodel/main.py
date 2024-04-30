import random
import joblib as jb
import numpy as np
from sklearn.preprocessing import StandardScaler
from process.db_update import UpdateDB
from process.load import load
from process.predict import predict
from process.train import train

filename = 'models/model.joblib'
# Load model
model = load(filename)

# Train model
model, X_test, y_test, y_pred, accuracy, report = train()
jb.dump(model, filename)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

new_data = np.array([[5.1, 3.5, 1.4, 0.2]])
new_data_scaled = StandardScaler().fit_transform(new_data)
prediction = predict(model, new_data_scaled)
print(f"Prediction for new data: {prediction}")

UpdateDB()

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Example data with team names and scores
csv_files = ['./data/historicalstats/2023.csv']
data = {
    'home_team': [],
    'away_team': [],
    'home_goals': [],
    'away_goals': [],
}
import csv

# Loop through CSV files
for csv_file in csv_files:
    # Load CSV file using pandas
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        rowcount = 1
        for row in csvreader:
            if rowcount != 1:
                data['home_team'].append(row[3])
                data['home_goals'].append(row[5])
                data['away_team'].append(row[4])
                data['away_goals'].append(row[6])
            rowcount += 1

# Convert data to DataFrame
df = pd.DataFrame(data)

# Concatenate home_team and away_team data
all_teams = pd.concat([df['home_team'], df['away_team']])
label_encoder = LabelEncoder()

# Fit LabelEncoder on concatenated home_team and away_team data
label_encoder.fit(all_teams)

# Encode team names using LabelEncoder
df['home_team_encoded'] = label_encoder.transform(df['home_team'])
df['away_team_encoded'] = label_encoder.transform(df['away_team'])
df.drop(['home_team', 'away_team'], axis=1, inplace=True)

# Determine match outcomes: 0 for draw, 1 for home team win, 2 for away team win
df['outcome'] = df.apply(lambda row: 0 if row['home_goals'] == row['away_goals'] else 1 if row['home_goals'] > row['away_goals'] else 2, axis=1)
X = df[['home_team_encoded', 'away_team_encoded', 'home_goals', 'away_goals']].values
y = df['outcome'].values

# Create and train a Logistic Regression classifier
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Make predictions for the new match
counts = {
    "hw": 0,
    "draw": 0,
    "aw": 0
}

for x in range(0, 500):
    new_match = {
        'home_team': ['Sheffield United'],
        'away_team': ['Man City'],
        'home_goals': [0],
        'away_goals': [0]
    }
    df_new_match = pd.DataFrame(new_match)
    
    # Encode team names
    df_new_match['home_team_encoded'] = label_encoder.transform(df_new_match['home_team'])
    df_new_match['away_team_encoded'] = label_encoder.transform(df_new_match['away_team'])
    df_new_match.drop(['home_team', 'away_team'], axis=1, inplace=True)
    
    # Extract features for the new match
    X_new_match = df_new_match[['home_team_encoded', 'away_team_encoded', 'home_goals', 'away_goals']].values
    prediction_new_match = model.predict(X_new_match)
    
    prediction_new_match += random.randint(-1, 1)
    prediction_new_match = max(0, min(2, prediction_new_match))
    
    # Print prediction
    if prediction_new_match == 1:
        counts['hw'] += 1
    elif prediction_new_match == 2:
        counts['aw'] += 1
    else:
        counts['draw'] += 1

print(counts)

threshold = 50

# Calculate the difference between home wins and away wins
diff_hw_aw = abs(counts['hw'] - counts['aw'])

if diff_hw_aw <= threshold:
    final_prediction = 'draw'
else:
    final_prediction = max(counts, key=counts.get)

print("Final Prediction:", final_prediction)

threshold = 50

# Calculate the difference between home wins and away wins
diff_hw_aw = abs(counts['hw'] - counts['aw'])

# Decide on the final prediction
if diff_hw_aw <= threshold:
    final_prediction = 'draw'  # Predict a draw for inconclusive matches
else:
    # Predict based on the majority class
    final_prediction = max(counts, key=counts.get)

print("Final Prediction:", final_prediction)