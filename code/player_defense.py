from nba_api.stats.endpoints import leagueseasonmatchups
# import json
import pandas as pd

team_map = {"ATL" : "Atlanta Hawks", "BKN" : "Brooklyn Nets", "BOS": "Boston Celtics", "CHA" : "Charlotte Hornets", "CHI" : "Chicago Bulls", "CLE" : "Cleveland Cavaliers", "DAL" : "Dallas Mavericks", "DEN" : "Denver Nuggets", "DET" : "Detroit Pistons", "GSW" : "Golden State Warriors", "HOU" : "Houston Rockets", "IND" : "Indiana Pacers", "LAC" : "Los Angeles Clippers", "LAL" : "Los Angeles Lakers", "MEM" : "Memphis Grizzlies", "MIA" : "Miami Heat", "MIL" : "Milwaukee Bucks", "MIN" : "Minnesota Timberwolves","NOP" : "New Orleans Pelicans", "NYK" : "New York Knicks", "OKC" : "Oklahoma City Thunder", "ORL" : "Orlando Magic", "PHI" : "Philadelphia 76ers", "PHX" : "Phoenix Suns", "POR" : "Portland Trail Blazers", "SAC" : "Sacramento Kings", "SAS" : "San Antonio Spurs", "TOR" : "Toronto Raptors", "UTA" : "Utah Jazz", "WAS" : "Washington Wizards"}

df_all_players = pd.read_csv('./player_data.csv')
df_team_data = pd.read_csv('../data/teams_stats/2019-20_nba_teams.csv')
i = 0

for index, row in df_all_players.iterrows():
    i += 1
    if i == 2:
        break
    playerid = row['ID']

    lsm_json = leagueseasonmatchups.LeagueSeasonMatchups(league_id = '00', 
    per_mode_simple = 'Totals', 
    season = '2019-20',
    season_type_playoffs = 'Regular Season', 
    def_player_id_nullable = str(playerid)).get_normalized_dict()

    df = pd.DataFrame(lsm_json["SeasonMatchups"])

    df['DOR_P'] = 0.
    df['DFG_P'] = 0.
    df['Stops1'] = 0.
    df['Stops2'] = 0.
    df['FMwt'] = 0.
    df['Stop_p'] = 0.
    df['DRtg'] = 0.
    df['Team_Defensive_Rating'] = 0.
    df['D_Pts_Per_ScPoss'] = 0.
    df['Team_Possessions'] = 0.

    for idx, r in df.iterrows():
        nextOffPlayerID = r['OFF_PLAYER_ID']
        playerTeam = team_map[row['Tm']]
        result = df_all_players[df_all_players['ID'].astype(str) == str(nextOffPlayerID)]
        if not result.empty:
            teamrow = df_team_data[df_team_data['Team'].str.match(playerTeam)]
            print(teamrow)
            print(result)
            df.at[idx, 'DOR_P'] = int(result['ORB']) / (result['ORB'] + int(teamrow['DRB']))
            df.at[idx, 'DFG_P'] = float(int(result['FG']) / int(result['FGA']))
            df.at[idx, 'FMwt'] = (df.iloc[idx]['DFG_P'] * (1 - df.at[idx, 'DOR_P'])) / (df.at[idx, 'DFG_P'] * (1 - df.at[idx, 'DOR_P']) + (1 - df.at[idx, 'DFG_P']) * df.at[idx, 'DOR_P'])
            df.at[idx, 'Stops1'] = row['STL'] + row['BLK'] * df.at[idx, 'FMwt'] * (1 - 1.07 * df.at[idx, 'DOR_P']) + row['DRB'] * (1 - df.at[idx, 'FMwt'])

            df.at[idx, 'Stops2'] = float((((int(result['FGA']) - int(result['FG']) - int(teamrow['BLK'])) / int(teamrow['MP'])) * float(df.at[idx, 'FMwt']) * (1 - 1.07 * float(df.at[idx, 'DOR_P'])) + 
            ((int(result['TOV']) - int(teamrow['STL'])) / int(teamrow['MP']))) * int(row['MP']) + int((row['PF']) / int(teamrow['PF'])) * 0.4 * int(result['FTA'] )* (1 - (int(result['FT']) / int(result['FTA'])))**2)

            df.at[idx, 'Team_Possessions'] = teamrow['FGA'] - teamrow['ORB'] + teamrow['TOV'] + (0.4 * teamrow['FTA'])

            df.at[idx, 'Stop_p'] = ((df.at[idx, 'Stops1'] + df.at[idx, 'Stops2']) * result['MP']) / (df.at[idx, 'Team_Possessions'] * row['MP'])

            df.at[idx, 'D_Pts_Per_ScPoss'] = result['PTS'] / (result['FG'] + (1 - (1 - (result['FT'] / result['FTA'])) ** 2) * result['FTA'] * 0.4)

            df.at[idx, 'Team_Defensive_Rating'] = 100 * (result['PTS'] / df.at[idx, 'Team_Possessions'])

            df.at[idx, 'DRtg'] = df.at[idx, 'Team_Defensive_Rating'] + 0.2 * (100 * df.at[idx, 'D_Pts_Per_ScPoss'] * (1 - df.at[idx, 'Stop_p']) - df.at[idx, 'Team_Defensive_Rating'])

            print(df.at[idx, 'DRtg'])
