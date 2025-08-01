from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
import torch
import joblib
import matplotlib.pyplot as plt
import io
import base64
from playernn import PlayerRatingLSTM

app = Flask(__name__)

# Configuration
INPUT_SIZE        = 40
MODEL_WEIGHTS     = 'player_nn_model_weights.pth'
SCALER_PATH       = 'scaler.pkl'
TEAM_DATA_PATH    = 'team.pkl'

# Load your best, pre-trained model (no training here)
model = PlayerRatingLSTM(input_size=INPUT_SIZE)
model.load_state_dict(torch.load(MODEL_WEIGHTS, map_location='cpu'))
model.eval()

# Load your pre-fitted scaler
scaler = joblib.load(SCALER_PATH)

def plot_goal_distribution(df):
    fig, ax = plt.subplots()
    df['Actual_Team_Goals'].plot(kind='hist', bins=range(0,8), ax=ax, alpha=0.7)
    ax.set(title="Team Goal Distribution", xlabel="Goals", ylabel="Frequency")
    buf = io.BytesIO()
    plt.tight_layout(); plt.savefig(buf, format='png'); plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET','POST'])
def index():
    error = None
    result_html = None
    plot_img = None

    # Prepare team list
    with open(TEAM_DATA_PATH, 'rb') as f:
        td = pickle.load(f)
    team_df  = td['team_df']
    match_df = td['match_df']
    ids = pd.unique(pd.concat([match_df.home_team_api_id, match_df.away_team_api_id]))
    names = sorted(team_df[team_df.team_api_id.isin(ids)].team_long_name.unique())

    if request.method == 'POST':
        csvfile = request.files.get('csvfile')
        if csvfile:
            try:
                df = pd.read_csv(csvfile)
                X  = df.drop(columns=['Actual_Team_Goals'], errors='ignore')
                Xs = scaler.transform(X)

                if Xs.shape[1] != INPUT_SIZE:
                    error = (f"Got {Xs.shape[1]} features; model expects {INPUT_SIZE}. "
                             "Please upload a CSV with the correct columns.")
                else:
                    Xt = torch.tensor(Xs, dtype=torch.float32).unsqueeze(1)
                    with torch.no_grad():
                        preds = model(Xt).squeeze().numpy()
                    df['Predicted_Team_Goals'] = np.rint(preds).astype(int)
                    result_html = df.to_html(classes='data', index=False)
                    plot_img    = plot_goal_distribution(df)

            except Exception as e:
                error = f"CSV processing error: {e}"

    return render_template('index.html',
                           team_names=names,
                           result=result_html,
                           plot_img=plot_img,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)




'''
def index():
    result = ""
    team_names = sorted(filtered_team_df['team_long_name'].unique())
    team_name = None
    start_date = ''
    end_date = ''

    if request.method == 'POST':
        team_name = request.form['team_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        print({team_name}, {start_date}, {end_date})
        
        # # === BEGIN core logic from your code === #
        # # Get team ID
        filtered_team = team_df[team_df['team_long_name'] == team_name]

        team_id = filtered_team['team_api_id'].values[0]

        # Filter matches
        team_matches = match_df[
            ((match_df['home_team_api_id'] == team_id) | (match_df['away_team_api_id'] == team_id)) &
            (match_df['date'] >= start_date) & (match_df['date'] <= end_date)
        ].copy()
        
        if team_matches.empty:
            return render_template('index.html', team_names=team_names, result="No matches found for that period.")

        # Compute perspective features
        team_matches['Venue'] = team_matches.apply(lambda row: 'Home' if row['home_team_api_id'] == team_id else 'Away', axis=1)
        team_matches['is_home'] = team_matches['Venue'].map({'Home': 1, 'Away': 0})
        team_matches['Opponent'] = team_matches.apply(
            lambda row: team_dict.get(row['away_team_api_id']) if row['Venue'] == 'Home' else team_dict.get(row['home_team_api_id']), axis=1
        )
        team_matches['team_goals'] = team_matches.apply(
            lambda row: row['home_team_goal'] if row['Venue'] == 'Home' else row['away_team_goal'], axis=1
        )
        team_matches['opponent_goals'] = team_matches.apply(
            lambda row: row['away_team_goal'] if row['Venue'] == 'Home' else row['home_team_goal'], axis=1
        )
        team_matches['prob_team'] = team_matches.apply(
            lambda row: row['prob_home'] if row['Venue'] == 'Home' else row['prob_away'], axis=1
        )
        team_matches['prob_opponent'] = team_matches.apply(
            lambda row: row['prob_away'] if row['Venue'] == 'Home' else row['prob_home'], axis=1
        )
        team_matches['betting_median_team'] = team_matches.apply(
            lambda row: row['betting_median_home'] if row['Venue'] == 'Home' else row['betting_median_away'], axis=1
        )
        team_matches['betting_median_opponent'] = team_matches.apply(
            lambda row: row['betting_median_away'] if row['Venue'] == 'Home' else row['betting_median_home'], axis=1
        )
        team_matches['avg_team_player_overall'] = team_matches.apply(
            lambda row: row['avg_home_player_overall'] if row['Venue'] == 'Home' else row['avg_away_player_overall'], axis=1
        )
        team_matches['avg_opponent_player_overall'] = team_matches.apply(
            lambda row: row['avg_away_player_overall'] if row['Venue'] == 'Home' else row['avg_home_player_overall'], axis=1
        )
        team_matches['Team_Form_Scored'] = team_matches.apply(
            lambda row: row['Home_Form_Scored'] if row['Venue'] == 'Home' else row['Away_Form_Scored'], axis=1
        )
        team_matches['Team_Form_Conceded'] = team_matches.apply(
            lambda row: row['Home_Form_Conceded'] if row['Venue'] == 'Home' else row['Away_Form_Conceded'], axis=1
        )
        team_matches['Opponent_Form_Scored'] = team_matches.apply(
            lambda row: row['Away_Form_Scored'] if row['Venue'] == 'Home' else row['Home_Form_Scored'], axis=1
        )
        team_matches['Opponent_Form_Conceded'] = team_matches.apply(
            lambda row: row['Away_Form_Conceded'] if row['Venue'] == 'Home' else row['Home_Form_Conceded'], axis=1
        )

        X_team = team_matches[[
            'prob_team', 'prob_draw', 'prob_opponent',
            'betting_median_team', 'betting_median_draw', 'betting_median_opponent',
            'Team_Form_Scored', 'Team_Form_Conceded', 'Opponent_Form_Scored', 'Opponent_Form_Conceded',
            'avg_team_player_overall', 'avg_opponent_player_overall', 'is_home'
        ]].rename(columns={
            'prob_team': 'prob_home',
            'prob_opponent': 'prob_away',
            'betting_median_team': 'betting_median_home',
            'betting_median_opponent': 'betting_median_away',
            'avg_team_player_overall': 'avg_home_player_overall',
            'avg_opponent_player_overall': 'avg_away_player_overall',
            'Team_Form_Scored': 'Home_Form_Scored',
            'Team_Form_Conceded': 'Home_Form_Conceded',
            'Opponent_Form_Scored': 'Away_Form_Scored',
            'Opponent_Form_Conceded': 'Away_Form_Conceded'
        })
        import torch

        # Reshape for LSTM: (batch_size, seq_len, input_size)
        # Here, assuming one timestep per match (seq_len = 1)
        X_tensor = torch.tensor(X_team.values, dtype=torch.float32).unsqueeze(1)  # shape: (N, 1, input_size)

        # Predict using LSTM model
        with torch.no_grad():
            y_pred_tensor = network(X_tensor).squeeze(1)  
        y_pred = np.round(y_pred_tensor.numpy()).astype(int)
        team_matches['Predicted_Team_Goals'] = np.round(y_pred).astype(int)
        team_matches['Predicted_Team_Goals'] = np.round(model_team_goals.predict(X_team)).astype(int)


        team_matches['Predicted_Opponent_Goals'] = team_matches.apply(
            lambda row: int(round(model_team_goals.predict([[
                row['prob_opponent'], row['prob_draw'], row['prob_team'],
                row['betting_median_opponent'], row['betting_median_draw'], row['betting_median_team'],
                row['Opponent_Form_Scored'], row['Opponent_Form_Conceded'], row['Team_Form_Scored'], row['Team_Form_Conceded'],
                row['avg_opponent_player_overall'], row['avg_team_player_overall'], 1 if row['Venue'] == 'Away' else 0
            ]])[0])), axis=1
        )

        team_matches['Actual_Team_Goals'] = team_matches['team_goals']
        team_matches['Actual_Opponent_Goals'] = team_matches['opponent_goals']

        def get_outcome(team_goals, opp_goals):
            if team_goals > opp_goals: return 'Win'
            elif team_goals == opp_goals: return 'Draw'
            else: return 'Loss'

        team_matches['Predicted_Outcome'] = team_matches.apply(
            lambda row: get_outcome(row['Predicted_Team_Goals'], row['Predicted_Opponent_Goals']), axis=1
        )
        team_matches['Actual_Outcome'] = team_matches.apply(
            lambda row: get_outcome(row['Actual_Team_Goals'], row['Actual_Opponent_Goals']), axis=1
        )
        
        # Calculate points
        def calculate_points(outcome):
            if outcome == "Win":
                return 3
            elif outcome =='Draw':
                return 1
            else:
                return 0

        # Create tables
        predictions_table = team_matches[['date', 'Opponent', 'Venue', 'Predicted_Team_Goals', 'Predicted_Opponent_Goals', 'Predicted_Outcome']]
        predictions_table['Predicted_Score'] = predictions_table['Predicted_Team_Goals'].astype(str) + ' - ' + predictions_table['Predicted_Opponent_Goals'].astype(str)

        actual_table = team_matches[['date', 'Opponent', 'Venue', 'Actual_Team_Goals', 'Actual_Opponent_Goals', 'Actual_Outcome']]
        actual_table['Actual_Score'] = actual_table['Actual_Team_Goals'].astype(str) + ' - ' + actual_table['Actual_Opponent_Goals'].astype(str)

        # Sort by date
        predictions_table = predictions_table.sort_values(by='date').reset_index(drop=True)
        actual_table = actual_table.sort_values(by='date').reset_index(drop=True)

        # Format dates
        predictions_table['date'] = pd.to_datetime(predictions_table['date']).dt.strftime('%Y-%m-%d')
        actual_table['date'] = pd.to_datetime(actual_table['date']).dt.strftime('%Y-%m-%d')
        
        predictions_html = predictions_table[['date', 'Opponent', 'Venue', 'Predicted_Score', 'Predicted_Outcome']].to_html(classes="table table-striped", index=False)
        actual_html = actual_table[['date', 'Opponent', 'Venue', 'Actual_Score', 'Actual_Outcome']].to_html(classes="table table-striped", index=False)

    
        
        num_matches = len(team_matches)
        actual_avg_team_goals = team_matches['Actual_Team_Goals'].mean()
        actual_avg_opp_goals = team_matches['Actual_Opponent_Goals'].mean()
        actual_record = team_matches['Actual_Outcome'].value_counts()
        predicted_avg_team_goals = team_matches['Predicted_Team_Goals'].mean()
        predicted_avg_opp_goals = team_matches['Predicted_Opponent_Goals'].mean()
        predicted_record = team_matches['Predicted_Outcome'].value_counts()

        # Calculate season scores
        actual_points = team_matches['Actual_Outcome'].map({'Win': 3, 'Draw': 1, 'Loss': 0}).sum()
        predicted_points = team_matches['Predicted_Outcome'].map({'Win': 3, 'Draw': 1, 'Loss': 0}).sum()

        # Calculate metrics
        mae_team = mean_absolute_error(team_matches['Actual_Team_Goals'], team_matches['Predicted_Team_Goals'])
        mae_opp = mean_absolute_error(team_matches['Actual_Opponent_Goals'], team_matches['Predicted_Opponent_Goals'])
        mse_team = mean_squared_error(team_matches['Actual_Team_Goals'], team_matches['Predicted_Team_Goals'])
        mse_opp = mean_squared_error(team_matches['Actual_Opponent_Goals'], team_matches['Predicted_Opponent_Goals'])
        rmse_team = np.sqrt(mse_team)
        rmse_opp = np.sqrt(mse_opp)
        r2_team = r2_score(team_matches['Actual_Team_Goals'], team_matches['Predicted_Team_Goals'])
        r2_opp = r2_score(team_matches['Actual_Opponent_Goals'], team_matches['Predicted_Opponent_Goals'])

        # Calculate outcome accuracy
        correct_outcomes = (team_matches['Actual_Outcome'] == team_matches['Predicted_Outcome']).sum()
        outcome_accuracy = (correct_outcomes / num_matches) * 100 if num_matches > 0 else 0

        result = f"""
        
        <h3>Results for {team_name} ({num_matches} matches from {start_date} to {end_date})</h3>
        <div style="display: flex; gap: 30px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px;">
                <h4>Actual Results</h4>
                {actual_html}
            </div>
            <div style="flex: 1; min-width: 300px;">
                <h4>Predicted Results</h4>
                {predictions_html}
            </div>
        </div>

        <hr>
        
        <h4>Actual Summary</h4>
        
        <ul>
            <li>Average Goals Scored by Team: {actual_avg_team_goals:.2f}</li>
            <li>Average Goals Conceded: {actual_avg_opp_goals:.2f}</li>
            <li>Record (W-D-L): {actual_record.get('Win', 0)}-{actual_record.get('Draw', 0)}-{actual_record.get('Loss', 0)}</li>
            <li>Season Score: {actual_points} points</li>
         </ul>
        <h4>Predicted Summary</h4>
        
        <ul>
            <li>Average Goals Scored by Team: {predicted_avg_team_goals:.2f}</li>
            <li>Average Goals Conceded: {predicted_avg_opp_goals:.2f}</li>
            <li>Record (W-D-L): {predicted_record.get('Win', 0)}-{predicted_record.get('Draw', 0)}-{predicted_record.get('Loss', 0)}</li>
            <li>Season Score: {predicted_points} points</li>
        </ul>
        
        <h4>Model Performance Metrics</h4>
        
        <ul>
            <li>Outcome Accuracy: {outcome_accuracy:.2f}%</li>
        </ul>
        """
        # === END core logic === #

    return render_template(
        'index.html',
        team_names=team_names,
        team_name=team_name,
        start_date=start_date,
        end_date=end_date,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)
'''