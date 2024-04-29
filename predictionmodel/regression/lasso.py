import pandas as pd
from sklearn import linear_model

def lasso_ex():

    # List of CSV files
    csv_files = ['./data/historicalstats/2023_modified.csv']

    # Select multiple features as independent variables
    home_team_features = ['HS', 'HC', 'AY', 'AR']
    away_team_features = ['AS', 'AC', 'HY', 'HR']
    important_variables = [['HST'], ['AST']]

    # Target column
    target_column = 'FTR'

    # Dictionary to store coefficients for each team
    team_coefficients = {}

    # Loop through CSV files
    for csv_file in csv_files:
        # Load CSV file using pandas
        df = pd.read_csv(csv_file)

        # Create a new column 'WeightedGoals' to represent the weighted goals
        df['WeightedGoals'] = df['FTHG'] - df['FTAG']

        # Iterate through unique team names
        unique_teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())

        for team_name in unique_teams:
            # Filter data for matches involving the current team
            team_home_data = df[(df['HomeTeam'] == team_name)]
            team_away_data = df[(df['AwayTeam'] == team_name)]

            # Check if there are any samples for the current team
            if team_home_data.shape[0] > 0 or team_away_data.shape[0] > 0:
                # Use team data for analysis
                team_home_X = team_home_data[home_team_features + important_variables[0] + ['WeightedGoals']].values
                team_home_y = team_home_data[target_column].values  # Keep as is

                team_away_X = team_away_data[away_team_features + important_variables[1] + ['WeightedGoals']].values
                team_away_y = team_away_data[target_column].values  # Keep as is

                # Create lasso regression objects
                regr_home = linear_model.Lasso(alpha=0.1)
                regr_home.fit(team_home_X, team_home_y)

                regr_away = linear_model.Lasso(alpha=0.1) 
                regr_away.fit(team_away_X, team_away_y)

                # Store coefficients for the current team
                team_coefficients[team_name] = {
                    'home_coefficients': regr_home.coef_.tolist(),
                    'away_coefficients': regr_away.coef_.tolist()
                }

    away_leaderboard_weighted = {}
    home_leaderboard_weighted = {}

    for team_name, coefficients in team_coefficients.items():
        home_coeff_avg = sum(map(abs, coefficients['home_coefficients'])) / len(coefficients['home_coefficients'])
        away_coeff_avg = sum(map(abs, coefficients['away_coefficients'])) / len(coefficients['away_coefficients'])

        # Count the number of away wins, home wins, and draws for the team
        num_away_wins = len(df[(df['AwayTeam'] == team_name) & (df['FTR'] == 1)])
        num_home_wins = len(df[(df['HomeTeam'] == team_name) & (df['FTR'] == 2)])
        num_draws = len(df[(df['HomeTeam'] == team_name) & (df['FTR'] == 0)]) + len(df[(df['AwayTeam'] == team_name) & (df['FTR'] == 0)])

        # Calculate the weighted average of absolute coefficients for away matches
        away_coeff_weighted_avg = away_coeff_avg * (num_away_wins + 0.5 * num_draws)
        away_leaderboard_weighted[team_name] = away_coeff_weighted_avg

        # Calculate the weighted average of absolute coefficients for home matches
        home_coeff_weighted_avg = home_coeff_avg * (num_home_wins + 0.5 * num_draws)
        home_leaderboard_weighted[team_name] = home_coeff_weighted_avg

    # Display away leaderboard
    sorted_away_leaderboard = sorted(away_leaderboard_weighted.items(), key=lambda x: x[1], reverse=True)
    print("Away Leaderboard (Weighted by Away Wins and Draws):")
    for rank, (team_name, score) in enumerate(sorted_away_leaderboard, start=1):
        print(f"{rank}. {team_name}: {score}")

    # Display home leaderboard
    sorted_home_leaderboard = sorted(home_leaderboard_weighted.items(), key=lambda x: x[1], reverse=True)
    print("\nHome Leaderboard (Weighted by Home Wins and Draws):")
    for rank, (team_name, score) in enumerate(sorted_home_leaderboard, start=1):
        print(f"{rank}. {team_name}: {score}")

    overall_leaderboard_weighted = {}

    for team_name in team_coefficients:
        # Sum the weighted averages for home and away matches
        overall_score = home_leaderboard_weighted.get(team_name, 0) + away_leaderboard_weighted.get(team_name, 0)
        overall_leaderboard_weighted[team_name] = overall_score

    # Display overall leaderboard
    sorted_overall_leaderboard = sorted(overall_leaderboard_weighted.items(), key=lambda x: x[1], reverse=True)
    print("\nOverall Leaderboard (Weighted by Home and Away Wins and Draws):")
    for rank, (team_name, score) in enumerate(sorted_overall_leaderboard, start=1):
        print(f"{rank}. {team_name}: {score}")

    return sorted_home_leaderboard, sorted_away_leaderboard, sorted_overall_leaderboard