import pandas as pd

def combine_pbp_and_rebound_logs_for_player_for_period(rebound_log_data, pbp_data, player_id, period, game_id):
    # adds PBP_EVENTNUM to rebound log data
    merged_rebounds = pd.DataFrame()
    pbp_player_period = pbp_data[(pbp_data['PERIOD'] == period) & (pbp_data['PLAYER1_ID'] == player_id) & (pbp_data['GAME_ID'] == game_id)]
    rebound_logs_player_period = rebound_log_data[(rebound_log_data['PERIOD'] == period) & (rebound_log_data['GAME_ID'] == game_id)]

    merged_rebounds = rebound_logs_player_period.set_index('REB_NUMBER')
    merged_rebounds['PBP_EVENTNUM'] = None

    pbp_split = pbp_player_period['PCTIMESTRING'].str.split(":")
    pbp_player_period['seconds'] = pbp_split.map(lambda x: int(x[0])*60 + int(x[1]))

    rebound_logs_split = rebound_logs_player_period['GAME_CLOCK'].str.split(":")
    rebound_logs_player_period['seconds'] = rebound_logs_split.map(lambda x: int(x[0])*60 + int(x[1]))

    pbp_player_period = pbp_player_period.sort('seconds', ascending=False)
    rebound_logs_player_period = rebound_logs_player_period.sort('seconds', ascending=False)

    pbp_player_period = pbp_player_period.reset_index(drop=True)
    rebound_logs_player_period = rebound_logs_player_period.reset_index(drop=True)

    # sometimes pbp has an extra rebound, find it and remove it
    if len(pbp_player_period.index) == len(rebound_logs_player_period.index) + 1:
        for i, row in pbp_player_period.iterrows():
            if i > len(rebound_logs_player_period.index)-1:
                pbp_player_period = pbp_player_period.drop(pbp_player_period.index[i])
                pbp_player_period = pbp_player_period.reset_index(drop=True)
                break
            elif abs(row['seconds'] - rebound_logs_player_period['seconds'].iloc[i]) > 5:
                pbp_player_period = pbp_player_period.drop(pbp_player_period.index[i])
                pbp_player_period = pbp_player_period.reset_index(drop=True)
                break

    # keep rebounds where times are within 5 seconds between datasets and rebound number for period is equal
    if len(pbp_player_period.index) == len(rebound_logs_player_period.index):
        for i, row in rebound_logs_player_period.iterrows():
            if abs(row['seconds'] - pbp_player_period['seconds'].iloc[i]) <= 5:
                merged_rebounds.loc[row['REB_NUMBER'],'PBP_EVENTNUM'] = int(pbp_player_period['EVENTNUM'].iloc[i])
    else:
        # when number of rebounds is different in both datasets, find rebounds within 5 seconds, if there is only 1, keep it
        for i, row in rebound_logs_player_period.iterrows():
            possible_matches = pbp_player_period[abs(row['seconds'] - pbp_player_period['seconds']) <= 5]
            if len(possible_matches.index) == 1 and len(rebound_logs_player_period[abs(row['seconds'] - rebound_logs_player_period['seconds']) <= 5]) == 1:
                merged_rebounds.loc[row['REB_NUMBER'],'PBP_EVENTNUM'] = int(possible_matches['EVENTNUM'].iloc[0])
    merged_rebounds['REB_NUMBER'] = merged_rebounds.index
    # convert nan to None to be inserted in MySQL db
    return pd.DataFrame.to_dict(merged_rebounds.where((pd.notnull(merged_rebounds)), None), 'records')
