import json
import requests
import pandas as pd
import scrape.helper

class Lineups:
    def __init__(self, game_data):
        self.moments_base_url = "http://stats.nba.com/stats/locations_getmoments/"
        self.boxscore_base_url = "http://stats.nba.com/stats/boxscore"
        self.game_data = game_data

    def get_players_on_floor_for_moment(self, game_id, event_id):
        # for a given game_id and event_id, return a dict with a list players on the floor for each team and team ids
        parameters = {
                        "gameid": game_id,
                        "eventid": event_id
        }
        response = requests.get(self.moments_base_url, params=parameters)
        data = response.json()
        players = {}
        players['home_team_id'] = data["moments"][0][5][1][0]
        players['away_team_id'] = data["moments"][0][5][6][0]
        players['home_player_ids'] =[]
        players['away_player_ids'] =[]
        for i in range(1,6):
            players['home_player_ids'].append(data["moments"][0][5][i][1])
        for i in range(6,11):
            players['away_player_ids'].append(data["moments"][0][5][i][1])
        return players

    def get_period_starters_from_boxscore(self, period, game_id, period_number):
        # get players who started period by getting time filtered box score for start of period until first sub
        home_team_id = period[(period['HOMEDESCRIPTION'].str.contains("MISS")) & (period['HOMEDESCRIPTION'] != None)]["PLAYER1_TEAM_ID"].min()
        visitor_team_id = period[(period['VISITORDESCRIPTION'].str.contains("MISS")) & (period['VISITORDESCRIPTION'] != None)]["PLAYER1_TEAM_ID"].min()

        split = period['PCTIMESTRING'].str.split(":")
        period['seconds'] = split.map(lambda x: int(x[0])*60 + int(x[1]))

        subs = period[(period['EVENTMSGTYPE'] == 8) & (period['PCTIMESTRING'] != "12:00")].index.tolist()

        if period_number == 1:
            start = "0000"
            if len(subs) > 0:
                end = (720-period['seconds'].iloc[subs[0]])*10
            else:
                end = (720-period["seconds"].iloc[-1])*10
        elif period_number <= 4:
            start = int(7200*(period_number-1))
            if len(subs) > 0:
                end = start + (720-period['seconds'].iloc[subs[0]])*10
            else:
                end = start + (720-period["seconds"].iloc[-1])*10
        else:
            start = int(28800 + 3000*(period_number-5))
            if len(subs) > 0:
                end = start + (300-period['seconds'].iloc[subs[0]])*10
            else:
                end = start + (300-period["seconds"].iloc[-1])*10

        period.drop('seconds', axis=1, inplace=True)

        boxscore_parameters = {
                                "GameID": game_id,
                                "StartRange": start,
                                "EndRange": end,
                                "RangeType": 2,
                                "StartPeriod": 0,
                                "EndPeriod": 0
        }

        period_starters = pd.DataFrame(scrape.helper.get_data_from_url_with_parameters(self.boxscore_base_url, boxscore_parameters, 4))

        split = period_starters['MIN'].str.split(":")
        period_starters['seconds'] = split.map(lambda x: int(x[0])*60 + int(x[1]))

        period_starters = period_starters.sort('seconds', ascending=False).head(10)

        players = {'home_player_ids': [], 'away_player_ids': []}

        for _, row in period_starters.iterrows():
            if str(row['TEAM_ID']) == str(home_team_id):
                players['home_player_ids'].append(row['PLAYER_ID'])
            else:
                players['away_player_ids'].append(row['PLAYER_ID'])
        return players


    def get_players_on_floor_for_period(self, period):
        # for a given period data frame, return a data frame with new columns for the players on the floor
        period = period.reset_index(drop=True)
        game_id = period['GAME_ID'].iloc[0]
        start_event_num = period[period['PCTIMESTRING'] != "12:00"]['EVENTNUM'].min()
        period_number = period['PERIOD'].mean()
        first_sub = period[period['EVENTMSGTYPE'] == 8]['EVENTNUM'].min()
        # while True:
        #     if start_event_num >= first_sub:
        #         period_starters = self.get_period_starters_from_boxscore(period, game_id, period_number)
        #         break
        #     try:
        #         period_starters = self.get_players_on_floor_for_moment(game_id, start_event_num)
        #         break
        #     except:
        #         start_event_num += 1
        period_starters = self.get_period_starters_from_boxscore(period, game_id, period_number)

        period['HOME_PLAYER1'] = period_starters['home_player_ids'][0]
        period['HOME_PLAYER2'] = period_starters['home_player_ids'][1]
        period['HOME_PLAYER3'] = period_starters['home_player_ids'][2]
        period['HOME_PLAYER4'] = period_starters['home_player_ids'][3]
        period['HOME_PLAYER5'] = period_starters['home_player_ids'][4]
        period['VISITOR_PLAYER1'] = period_starters['away_player_ids'][0]
        period['VISITOR_PLAYER2'] = period_starters['away_player_ids'][1]
        period['VISITOR_PLAYER3'] = period_starters['away_player_ids'][2]
        period['VISITOR_PLAYER4'] = period_starters['away_player_ids'][3]
        period['VISITOR_PLAYER5'] = period_starters['away_player_ids'][4]

        # get index for all substitutions and for each one sub in and out appropriate players
        subs = period[period['EVENTMSGTYPE'] == 8].index.tolist()
        end = len(period.index)
        for i in range(len(subs)):
            if str(period['HOME_PLAYER1'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'HOME_PLAYER1'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['HOME_PLAYER2'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'HOME_PLAYER2'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['HOME_PLAYER3'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'HOME_PLAYER3'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['HOME_PLAYER4'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'HOME_PLAYER4'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['HOME_PLAYER5'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'HOME_PLAYER5'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['VISITOR_PLAYER1'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'VISITOR_PLAYER1'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['VISITOR_PLAYER2'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'VISITOR_PLAYER2'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['VISITOR_PLAYER3'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'VISITOR_PLAYER3'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['VISITOR_PLAYER4'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'VISITOR_PLAYER4'] = str(period['PLAYER2_ID'][subs[i]])
            elif str(period['VISITOR_PLAYER5'].iloc[subs[i]]) == str(period['PLAYER1_ID'][subs[i]]):
                period.ix[subs[i]:end, 'VISITOR_PLAYER5'] = str(period['PLAYER2_ID'][subs[i]])
        return period

    def get_players_on_floor_for_game(self):
        players_on_floor_df = self.game_data.groupby("PERIOD").apply(self.get_players_on_floor_for_period)
        # convert nan values to None to be inserted in MySQL db
        return pd.DataFrame.to_dict(players_on_floor_df.where((pd.notnull(players_on_floor_df)), None), 'records')
