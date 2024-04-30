import pandas as pd
import h2o
from h2o.automl import H2OAutoML

# Initialize H2O cluster
h2o.init()

# Load data
data = pd.read_csv("data/historicalstats/2023.csv")
h2o_data = h2o.H2OFrame(data)

# Define features and target
ftr_features = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']
hg_features = ['HomeTeam', 'AwayTeam', 'FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']
ag_features = ['HomeTeam', 'AwayTeam', 'FTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']

# Initialize AutoML
# ftr_model = H2OAutoML(max_runtime_secs=600)  # 10 mins runtime
# ftr_model.train(x=ftr_features, y='FTR', training_frame=h2o_data)
# hg_model = H2OAutoML(max_runtime_secs=600)  # 10 mins runtime
# hg_model.train(x=hg_features, y='FTHG', training_frame=h2o_data)
# ag_model = H2OAutoML(max_runtime_secs=600)  # 10 mins runtime
# ag_model.train(x=ag_features, y='FTAG', training_frame=h2o_data)

ftr_model = h2o.load_model('./models/ftr/StackedEnsemble_AllModels_4_AutoML_1_20240429_142547')
hg_model = h2o.load_model('./models/hg/StackedEnsemble_BestOfFamily_7_AutoML_2_20240429_143551')
ag_model = h2o.load_model('./models/ag/GLM_1_AutoML_3_20240429_144604')

# ftr_model = ftr_model.leader
# h2o.save_model(ftr_model, path="./models/ftr", force=True)
# hg_model = hg_model.leader
# h2o.save_model(hg_model, path="./models/hg", force=True)
# ag_model = ag_model.leader
# h2o.save_model(ag_model, path="./models/ag", force=True)

import random

teams = [
    "Burnley", "Man City", "Arsenal", "Chelsea", "Tottenham", "Aston Villa", "Brentford", "Brighton", "Fulham", "West Ham", "Nott'm Forest",
    "Bournemouth", "Wolves", "Sheffield United", "Newcastle", "Luton", "Crystal Palace"
]

team1 = teams[random.randint(0, len(teams)-1)]
team2 = teams[random.randint(0, len(teams)-1)]
# Make predictions for future games
future_data = h2o.H2OFrame({"HomeTeam": [team1], "AwayTeam": [team2]})

ftr_prediction = ftr_model.predict(future_data)
hg_prediction = hg_model.predict(future_data)
ag_prediction = ag_model.predict(future_data)
hg_num = hg_prediction[0, 0]
ag_num = ag_prediction[0, 0]
A_prob = ftr_prediction[0, 'A']
D_prob = ftr_prediction[0, 'D']
H_prob = ftr_prediction[0, 'H']
# BASE A-> 0.05  D->0.67  H->0.28
if max(A_prob-0.05, D_prob-0.67, H_prob-0.28) == A_prob-0.05: print(A_prob-0.05, D_prob-0.67, H_prob-0.28, team1, team2, hg_num, ag_num, "AWAY WIN")
elif max(A_prob-0.05, D_prob-0.67, H_prob-0.28) == D_prob-0.67: print(A_prob-0.05, D_prob-0.67, H_prob-0.28, team1, team2, hg_num, ag_num, "DRAW")
else: print(A_prob-0.05, D_prob-0.67, H_prob-0.28, team1, team2, hg_num, ag_num, "HOME WIN")

# future_data = h2o.H2OFrame({"HomeTeam": [teams[random.randint(0, len(teams)-1)]], "AwayTeam": [teams[random.randint(0, len(teams)-1)]], 
# "FTHG": [0], "FTAG": [0], "HTHG": [0], "HTAG": [0], "HS": [2], "AS": [0], 
# "HST": [0], "AST": [0], "HF": [0], "AF": [0], "HC": [0], "AC": [0], 
# "HY": [0], "AY": [0], "HR": [0], "AR": [0], "B365H": [0], "B365D": [0], 
# "B365A": [0]})

h2o.cluster().shutdown()