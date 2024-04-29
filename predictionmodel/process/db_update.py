import json
import random
import psycopg2
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime
from fuzzywuzzy import fuzz

from regression.linear_ex import linear_ex
from regression.lasso import lasso_ex

load_dotenv()

# STANDARD UPDATE DB FOR TEMP SCORES IN ALGORITHM PREDICTION TABLE 

def UpdateDB():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
                
    cur.execute("SELECT COUNT(*) FROM prempredict_AlgorithmPrediction")
    count = int(''.join(filter(str.isdigit, str(cur.fetchall()))))
    print(count)

    if count != 38:
        gameweekcounter = 1
        cur.execute("DELETE FROM prempredict_AlgorithmPrediction")
        while gameweekcounter <= 38:
            cur.execute("INSERT INTO prempredict_AlgorithmPrediction (gameweek, scores, date) VALUES (%s, %s, %s)", (gameweekcounter, json.dumps({}), datetime.now()))
            gameweekcounter += 1

    # Only update when gameweek > current gameweek
    cur.execute("SELECT * FROM prempredict_PremSeasonInfo WHERE active = true")
    currentMatchday = cur.fetchone()[2]
    cur.execute("SELECT deadline FROM prempredict_PremGameweeks WHERE number = " + str(currentMatchday))
    deadline_datetime = datetime.strptime(str(cur.fetchone()[0]), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
    current_datetime = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/London'))

    while current_datetime >= deadline_datetime:
        currentMatchday += 1
        cur.execute("SELECT deadline FROM prempredict_PremGameweeks WHERE number = " + str(currentMatchday))
        deadline_datetime = datetime.strptime(str(cur.fetchone()[0]), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
        current_datetime = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/London'))

    currentMatchday+=1

    sorted_home, sorted_away, sorted_overall = lasso_ex()
    print(sorted_home, sorted_away, sorted_overall)

    sorted_home, sorted_away, sorted_overall = linear_ex()
    print(sorted_home, sorted_away, sorted_overall)

    #currentMatchday=1
    while currentMatchday <= 38:
        print(currentMatchday)
        gameweek_scores = {}
        cur.execute("SELECT matchid FROM prempredict_PremGames WHERE matchday = (%s)", (currentMatchday,))
        records = cur.fetchall()

        matchid_dict = {record[0]: None for record in records}
        # get home and away teams for that matchid
        query = """
            SELECT
                home_team.fullname as home_team_name,
                away_team.fullname as away_team_name
            FROM
                prempredict_premgames AS game
            INNER JOIN
                prempredict_premteams AS home_team ON game.hometeam_id = home_team.id
            INNER JOIN
                prempredict_premteams AS away_team ON game.awayteam_id = away_team.id
            WHERE
                game.matchday = %s
        """
        cur.execute(query, [currentMatchday])
        result = cur.fetchall()
        i = 0
        for matchid in matchid_dict:

            home_team_name, away_team_name = result[i]
            home_rank_value = max(sorted_home, key=lambda x: fuzz.ratio(home_team_name.lower(), x[0].lower()))[1] 
            home_overall_rank_value = max(sorted_overall, key=lambda x: fuzz.ratio(home_team_name.lower(), x[0].lower()))[1] 
            away_rank_value = max(sorted_away, key=lambda x: fuzz.ratio(away_team_name.lower(), x[0].lower()))[1]
            away_overall_rank_value = max(sorted_overall, key=lambda x: fuzz.ratio(away_team_name.lower(), x[0].lower()))[1]

            value_prediction_difference = ((home_rank_value+home_overall_rank_value)/2) - ((away_rank_value+away_overall_rank_value)/2)

            print([home_team_name, away_team_name, value_prediction_difference])

            home_prediction = max(0, int(random.randint(0, 2) + (value_prediction_difference)))
            away_prediction = max(0, int(random.randint(0, 2) - (value_prediction_difference/1.1)))
            # predict scores using model
            gameweek_scores[matchid] = {'home': home_prediction, 'away': away_prediction}

            i+=1

        print(gameweek_scores)
        cur.execute("UPDATE prempredict_AlgorithmPrediction SET scores = %s, date = %s WHERE gameweek = %s", (json.dumps(gameweek_scores), datetime.now(), currentMatchday))
        currentMatchday += 1

    conn.commit()
    cur.close()
    conn.close()
