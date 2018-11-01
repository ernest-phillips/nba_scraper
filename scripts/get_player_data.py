import json
import logging
import sys
import re
import time
import pandas as pd
from sqlalchemy import create_engine, distinct
from sqlalchemy.sql import select, and_, or_

from scrape import player_stats, sportvu_stats
from storage import schema
from utils import utils
from process import combine_pbp_shot_logs, combine_pbp_rebounds_logs

def main():
    logging.basicConfig(filename='logs/players.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config=json.loads(open('config.json').read())

    season = config["season"]
    is_regular_season = config["is_regular_season"]
    # make sure season is valid format
    season_pattern = re.compile('\d{4}[-]\d{2}$')
    if season_pattern.match(season) == None:
        print "Invalid Season format. Example format: 2014-15"
        sys.exit(0)

    if is_regular_season == 0:
        season_type = "Playoffs"
        game_prefix = "004"
    elif is_regular_season == 1:
        season_type = "Regular Season"
        game_prefix = "002"
    else:
        print "Invalid is_regular_season value. Use 0 for regular season, 1 for playoffs"
        sys.exit(0)

    # connect to database
    username = config['username']
    password = config['password']
    host = config['host']
    database = config['database']

    engine = create_engine('mysql://'+username+':'+password+'@'+host+'/'+database)
    conn = engine.connect()

    # get player_ids to update
    players_to_update = {}
    games_in_db_query = select([distinct(schema.player_tracking_shot_logs.c.GAME_ID)]).where(schema.player_tracking_shot_logs.c.GAME_ID.ilike(game_prefix+"%"))
    players_to_update_query = select([schema.traditional_boxscores.c.PLAYER_ID, schema.traditional_boxscores.c.PLAYER_NAME]).where(and_(schema.traditional_boxscores.c.GAME_ID.notin_(games_in_db_query), schema.traditional_boxscores.c.GAME_ID.ilike(game_prefix+"%"))).distinct()

    for player in conn.execute(players_to_update_query):
        players_to_update[player.PLAYER_ID] = player.PLAYER_NAME

    if len(players_to_update.keys()) == 0:
        players_to_update_query = select([schema.traditional_boxscores.c.PLAYER_ID, schema.traditional_boxscores.c.PLAYER_NAME]).where(and_(schema.traditional_boxscores.c.FGA > 0, schema.traditional_boxscores.c.GAME_ID.ilike(game_prefix+"%"))).distinct()
        for player in conn.execute(players_to_update_query):
            players_to_update[player.PLAYER_ID] = player.PLAYER_NAME

    # get and update data
    for player_id in players_to_update.keys():
        if int(player_id) > 0 and int(player_id) < 2147483647:
            player_name = players_to_update[player_id]
            player_data = player_stats.PlayerData(player_id, player_name, season, season_type)
            try:
                # get shot logs
                player_shot_logs = player_data.shot_logs()
                player_shot_logs_df = pd.DataFrame(player_shot_logs)
                if len(player_shot_logs_df.index) > 0:
                    games_and_periods = player_shot_logs_df[['GAME_ID', 'PERIOD']]
                    unique_games_and_periods = games_and_periods.drop_duplicates()

                    # get shots already in db
                    already_in_db_query = select([schema.player_tracking_shot_logs.c.GAME_ID, schema.player_tracking_shot_logs.c.PERIOD]).where(schema.player_tracking_shot_logs.c.PLAYER_ID == player_id).distinct()
                    for period_game in conn.execute(already_in_db_query):
                        already_in = (unique_games_and_periods.GAME_ID == period_game.GAME_ID) & (unique_games_and_periods.PERIOD == period_game.PERIOD)
                        unique_games_and_periods = unique_games_and_periods[already_in == False]

                    if len(unique_games_and_periods.index) > 0:
                        # merge shot logs with pbp_data
                        pbp_query = select([(schema.pbp)]).where(and_(schema.pbp.c.PLAYER1_ID == player_id, or_(schema.pbp.c.EVENTMSGTYPE == 1, schema.pbp.c.EVENTMSGTYPE == 2)))
                        results = conn.execute(pbp_query)
                        pbp_data = pd.DataFrame(results.fetchall())
                        pbp_data.columns = results.keys()
                        for _, row in unique_games_and_periods.iterrows():
                            shots = combine_pbp_shot_logs.combine_pbp_and_shot_logs_for_player_for_period(player_shot_logs_df, pbp_data, player_id, row['PERIOD'], row['GAME_ID'])
                            conn.execute(schema.player_tracking_shot_logs.insert(replace_string=""), shots)
            except:
                logging.error(utils.LogException())

            try:
                # get rebound logs
                player_rebound_logs = player_data.rebound_logs()
                player_rebound_logs_df = pd.DataFrame(player_rebound_logs)
                if len(player_rebound_logs_df.index) > 0:
                    games_and_periods = player_rebound_logs_df[['GAME_ID', 'PERIOD']]
                    unique_games_and_periods = games_and_periods.drop_duplicates()

                    # get rebounds already in db
                    already_in_db_query = select([schema.player_tracking_rebound_logs.c.GAME_ID, schema.player_tracking_rebound_logs.c.PERIOD]).where(schema.player_tracking_rebound_logs.c.PLAYER_ID == player_id).distinct()
                    for period_game in conn.execute(already_in_db_query):
                        already_in = (unique_games_and_periods.GAME_ID == period_game.GAME_ID) & (unique_games_and_periods.PERIOD == period_game.PERIOD)
                        unique_games_and_periods = unique_games_and_periods[already_in == False]

                    if len(unique_games_and_periods.index) > 0:
                        # merge rebound logs with pbp_data
                        pbp_query = select([(schema.pbp)]).where(and_(schema.pbp.c.PLAYER1_ID == player_id, schema.pbp.c.EVENTMSGTYPE == 4))
                        results = conn.execute(pbp_query)
                        pbp_data = pd.DataFrame(results.fetchall())
                        pbp_data.columns = results.keys()
                        for _, row in unique_games_and_periods.iterrows():
                            rebounds = combine_pbp_rebounds_logs.combine_pbp_and_rebound_logs_for_player_for_period(player_rebound_logs_df, pbp_data, player_id, row['PERIOD'], row['GAME_ID'])
                            conn.execute(schema.player_tracking_rebound_logs.insert(replace_string=""), rebounds)
            except:
                logging.error(utils.LogException())

            try:
                conn.execute(schema.player_tracking_passes_made.insert(replace_string=""), utils.add_keys(player_data.passes_made(), time.strftime("%Y-%m-%d"), is_regular_season))
            except:
                logging.error(utils.LogException())

            try:
                conn.execute(schema.player_tracking_passes_received.insert(replace_string=""), utils.add_keys(player_data.passes_received(), time.strftime("%Y-%m-%d"), is_regular_season))
            except:
                logging.error(utils.LogException())

if __name__ == '__main__':
    main()
