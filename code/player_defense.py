from nba_api.stats.endpoints import leagueseasonmatchups
# import json
import pandas as pd

df_all_players = pd.read_csv('player_data.csv')

# for index, row in df_all_players.iterrows():
#     playerid = row['ID']
#     lsm_json = leagueseasonmatchups.LeagueSeasonMatchups(league_id = '00', per_mode_simple = 'Totals', season = '2019-20', season_type_playoffs = 'Regular Season', def_player_id_nullable = playerid).get_normalized_dict()

# json_object = json.dumps(lsm_json)

# with open("normal.json", "w") as outfile:
#     outfile.write(json_object)

# data = json.load(json_object)

lsm_json = leagueseasonmatchups.LeagueSeasonMatchups(league_id = '00', per_mode_simple = 'Totals', season = '2019-20', season_type_playoffs = 'Regular Season', def_player_id_nullable = '2544').get_normalized_dict()

df = pd.DataFrame(lsm_json["SeasonMatchups"])

# df = df[['OFF_PLAYER_ID','MATCHUP_MIN','PARTIAL_POSS','PLAYER_PTS','TEAM_PTS','MATCHUP_TOV','MATCHUP_BLK','MATCHUP_FGA','MATCHUP_FG3A']]

# df.columns = ['off_player_id','matchup_min','poss','player_pts','team_pts','tov','blk','fga','fg3a']

# df['fg2a'] = df.fga - df.fg3a

# xFta = 

df.to_csv('pleasework.csv')