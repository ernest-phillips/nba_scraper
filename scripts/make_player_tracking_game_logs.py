# make player tracking game logs for date range, if no dates entered gets yesterday, date format YYYY-MM-DD separated by a space
import json
import logging
import sys
import re
import datetime
from dateutil.rrule import rrule, DAILY
import time
from sqlalchemy import create_engine
from sqlalchemy.sql import select

from scrape import sportvu_stats
from storage import schema
from utils import utils

def store_player_stat(season, season_type, measure_type, request_date, game_date, game_ids, game_player_map, is_regular_season, table, connection):
    try:
        player_stats = sportvu_stats.get_sportvu_data_for_stat(season, season_type, "Player", measure_type, start_date=request_date, end_date=request_date)
        game_date_with_game_id = sportvu_stats.add_game_id_to_game_log_for_player(player_stats, game_date, game_ids, game_player_map)
        connection.execute(table.insert(replace_string=""), utils.add_keys(game_date_with_game_id, game_date, is_regular_season))
    except:
        logging.error(utils.LogException())
    return None

def store_team_stat(season, season_type, measure_type, request_date, game_date, game_ids, game_team_map, is_regular_season, table, connection):
    try:
        team_stats = sportvu_stats.get_sportvu_data_for_stat(season, season_type, "Team", measure_type, start_date=request_date, end_date=request_date)
        team_stats_with_game_id = sportvu_stats.add_game_id_to_game_log_for_team(team_stats, game_date, game_ids, game_team_map)
        connection.execute(table.insert(replace_string=""), utils.add_keys(team_stats_with_game_id, game_date, is_regular_season))
    except:
        logging.error(utils.LogException())
    return None

def main():
    logging.basicConfig(filename='logs/player_tracking_game_logs.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config=json.loads(open('config.json').read())

    # validate data
    if len(sys.argv) < 3:
        start_date = datetime.date.today() - datetime.timedelta(1)
        end_date = datetime.date.today() - datetime.timedelta(1)
    elif len(sys.argv) > 3:
        print "Too many arguments. Enter a start and end date with format YYYY-MM-DD"
        sys.exit(0)
    else:
        start = sys.argv[1]
        end = sys.argv[2]
        # validate dates
        try:
            datetime.datetime.strptime(start, '%Y-%m-%d')
        except:
            print 'invalid format for start date'
            sys.exit(0)

        try:
            datetime.datetime.strptime(end, '%Y-%m-%d')
        except:
            print 'invalid format for end date'
            sys.exit(0)

        start_split = start.split("-")
        end_split = end.split("-")

        start_date = datetime.date(int(start_split[0]), int(start_split[1]), int(start_split[2]))
        end_date = datetime.date(int(end_split[0]), int(end_split[1]), int(end_split[2]))

    season = config["season"]
    is_regular_season = config["is_regular_season"]
    # make sure season is valid format
    season_pattern = re.compile('\d{4}[-]\d{2}$')
    if season_pattern.match(season) == None:
        print "Invalid Season format. Example format: 2014-15"
        sys.exit(0)
    year = season.split("-")[0]

    if is_regular_season == 0:
        season_type = "Playoffs"
    elif is_regular_season == 1:
        season_type = "Regular Season"
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

    # create maps to get game id from game date
    game_player_map = {}
    boxscore_player_query = select([schema.traditional_boxscores.c.GAME_ID, schema.traditional_boxscores.c.PLAYER_ID, schema.traditional_boxscores.c.TEAM_ID])
    for player_line in conn.execute(boxscore_player_query):
        if player_line[1] in game_player_map.keys():
            game_player_map[player_line[1]][player_line[0]] = player_line[2]
        else:
            game_player_map[player_line[1]] = {player_line[0]:player_line[2]}

    game_team_map = {}
    boxscore_team_query = select([schema.traditional_boxscores_team.c.GAME_ID, schema.traditional_boxscores_team.c.TEAM_ID])
    for team_line in conn.execute(boxscore_team_query):
        if team_line[1] in game_team_map.keys():
            game_team_map[team_line[1]][team_line[0]] = None
        else:
            game_team_map[team_line[1]] = {team_line[0]:None}

    # get data
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        day = dt.strftime("%d")
        month = dt.strftime("%m")
        year = dt.strftime("%Y")

        date = month + "/" + day + "/" + year
        date_to_store = year + "-" + month + "-" + day
        game_date_est = date_to_store + 'T00:00:00'

        games_query = select([schema.game_summary.c.GAME_ID]).where(schema.game_summary.c.GAME_DATE_EST == game_date_est)
        games = conn.execute(games_query)

        game_ids = []
        for game in games:
            game_ids.append(game[0])

        store_player_stat(season, season_type, "CatchShoot", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_catch_shoot_game_logs, conn)
        store_team_stat(season, season_type, "CatchShoot", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_catch_shoot_team_game_logs, conn)
        store_player_stat(season, season_type, "Defense", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_defense_game_logs, conn)
        store_team_stat(season, season_type, "Defense", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_defense_team_game_logs, conn)
        store_player_stat(season, season_type, "Drives", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_drives_game_logs, conn)
        store_team_stat(season, season_type, "Drives", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_drives_team_game_logs, conn)
        store_player_stat(season, season_type, "Passing", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_passing_game_logs, conn)
        store_team_stat(season, season_type, "Passing", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_passing_team_game_logs, conn)
        store_player_stat(season, season_type, "PullUpShot", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_pull_up_shoot_game_logs, conn)
        store_team_stat(season, season_type, "PullUpShot", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_pull_up_shoot_team_game_logs, conn)
        store_player_stat(season, season_type, "Rebounding", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_rebounding_game_logs, conn)
        store_team_stat(season, season_type, "Rebounding", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_rebounding_team_game_logs, conn)
        store_player_stat(season, season_type, "Efficiency", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_shooting_game_logs, conn)
        store_team_stat(season, season_type, "Efficiency", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_shooting_team_game_logs, conn)
        store_player_stat(season, season_type, "SpeedDistance", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_speed_game_logs, conn)
        store_team_stat(season, season_type, "SpeedDistance", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_speed_team_game_logs, conn)
        store_player_stat(season, season_type, "ElbowTouch", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_elbow_touches_game_logs, conn)
        store_team_stat(season, season_type, "ElbowTouch", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_elbow_touches_team_game_logs, conn)
        store_player_stat(season, season_type, "PaintTouch", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_paint_touches_game_logs, conn)
        store_team_stat(season, season_type, "PaintTouch", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_paint_touches_team_game_logs, conn)
        store_player_stat(season, season_type, "PostTouch", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_post_touches_game_logs, conn)
        store_team_stat(season, season_type, "PostTouch", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_post_touches_team_game_logs, conn)
        store_player_stat(season, season_type, "Possessions", date, date_to_store, game_ids, game_player_map, is_regular_season, schema.sportvu_possessions_game_logs, conn)
        store_team_stat(season, season_type, "Possessions", date, date_to_store, game_ids, game_team_map, is_regular_season, schema.sportvu_possessions_team_game_logs, conn)

if __name__ == '__main__':
    main()
