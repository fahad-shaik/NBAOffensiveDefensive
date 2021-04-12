from nba_api.stats.endpoints import leagueseasonmatchups
# import json
import pandas as pd

df_all_players = pd.read_csv('./player_data.csv')

# for index, row in df_all_players.iterrows():
#     playerid = row['ID']
#     lsm_json = leagueseasonmatchups.LeagueSeasonMatchups(league_id = '00', per_mode_simple = 'Totals', season = '2019-20', season_type_playoffs = 'Regular Season', def_player_id_nullable = playerid).get_normalized_dict()

# json_object = json.dumps(lsm_json)

# with open("normal.json", "w") as outfile:
#     outfile.write(json_object)

# data = json.load(json_object)

lsm_json = leagueseasonmatchups.LeagueSeasonMatchups(league_id = '00', 
per_mode_simple = 'Totals', 
season = '2019-20',
season_type_playoffs = 'Regular Season', 
def_player_id_nullable = str(1628401)).get_normalized_dict()

df = pd.DataFrame(lsm_json["SeasonMatchups"])

# print(df.columns)

df = df[['OFF_PLAYER_ID','MATCHUP_MIN','PARTIAL_POSS','PLAYER_PTS','TEAM_PTS','MATCHUP_TOV','MATCHUP_BLK','MATCHUP_FGA','MATCHUP_FG3A']]

df['FTA'] = 0
df['TOV'] = 0
df['BLK'] = 0
df['FG2M'] = 0
df['FG3M'] = 0
df['FTM'] = 0

# print(df.loc[0])

# df_all_players['ID'].astype(str)

def getOtherCols():
    for idx, r in df.iterrows():
        nextOffPlayerID = r['OFF_PLAYER_ID']
        result = df_all_players[df_all_players['ID'].astype(str) == str(nextOffPlayerID)]
        if not result.empty:
            df.at[idx,'FTA'] = int(result['FTA']) // 100
            df.at[idx,'TOV'] = int(result['TOV']) // 100
            df.at[idx,'BLK'] = int(result['BLK']) / 100
            df.at[idx,'FG2M'] = int(result['2P'])
            df.at[idx,'FG3M'] = int(result['3P'])
            df.at[idx,'FTM'] = int(result['FT'])

getOtherCols()

# df['x_pts'] = ((df.x_fg2m * 2) + (df.x_fg3m * 3) + (df.x_ftm * 1)) - df.x_blk - df.x_tov

df['PTS'] = ((df['FG2M']*2) + (df['FG3M']*3) + (df['FTM']*1)) - df['BLK'] - df['TOV']
# print(df.loc[0])

# df['val'] = df.x_pts - (df.player_pts - df.blk - df.tov)

df['VAL'] = df['PTS'] - df['PLAYER_PTS'] - df['BLK'] - df['TOV']
print(df.loc[0])

print(df['VAL'].sum())
print(df['PARTIAL_POSS'].sum())
dps = (df['VAL'].sum() / df['PARTIAL_POSS'].sum()) * 100
print(dps)
