import json
import logging
import sys
import re
import time
from sqlalchemy import create_engine

from utils import utils
from storage import schema
from scrape import sportvu_stats

def store_stat(season, season_type, player_or_team, measure_type, is_regular_season, table, connection):
    try:
        stat_data = sportvu_stats.get_sportvu_data_for_stat(season, season_type, player_or_team, measure_type)
        connection.execute(table.insert(replace_string=""), utils.add_keys(stat_data, time.strftime("%Y-%m-%d"), is_regular_season))
    except:
        logging.error(utils.LogException())
    return None

def main():
    logging.basicConfig(filename='logs/sportvu.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config=json.loads(open('config.json').read())

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

    username = config['username']
    password = config['password']
    host = config['host']
    database = config['database']

    engine = create_engine('mysql://'+username+':'+password+'@'+host+'/'+database)
    conn = engine.connect()

    store_stat(season, season_type, "Player", "CatchShoot", is_regular_season, schema.sportvu_catch_shoot, conn)
    store_stat(season, season_type, "Team", "CatchShoot", is_regular_season, schema.sportvu_catch_shoot_team, conn)
    store_stat(season, season_type, "Player", "Defense", is_regular_season, schema.sportvu_defense, conn)
    store_stat(season, season_type, "Team", "Defense", is_regular_season, schema.sportvu_defense_team, conn)
    store_stat(season, season_type, "Player", "Drives", is_regular_season, schema.sportvu_drives, conn)
    store_stat(season, season_type, "Team", "Drives", is_regular_season, schema.sportvu_drives_team, conn)
    store_stat(season, season_type, "Player", "Passing", is_regular_season, schema.sportvu_passing, conn)
    store_stat(season, season_type, "Team", "Passing", is_regular_season, schema.sportvu_passing_team, conn)
    store_stat(season, season_type, "Player", "PullUpShot", is_regular_season, schema.sportvu_pull_up_shoot, conn)
    store_stat(season, season_type, "Team", "PullUpShot", is_regular_season, schema.sportvu_pull_up_shoot_team, conn)
    store_stat(season, season_type, "Player", "Rebounding", is_regular_season, schema.sportvu_rebounding, conn)
    store_stat(season, season_type, "Team", "Rebounding", is_regular_season, schema.sportvu_rebounding_team, conn)
    store_stat(season, season_type, "Player", "Efficiency", is_regular_season, schema.sportvu_shooting, conn)
    store_stat(season, season_type, "Team", "Efficiency", is_regular_season, schema.sportvu_shooting_team, conn)
    store_stat(season, season_type, "Player", "SpeedDistance", is_regular_season, schema.sportvu_speed, conn)
    store_stat(season, season_type, "Team", "SpeedDistance", is_regular_season, schema.sportvu_speed_team, conn)
    store_stat(season, season_type, "Player", "ElbowTouch", is_regular_season, schema.sportvu_elbow_touches, conn)
    store_stat(season, season_type, "Team", "ElbowTouch", is_regular_season, schema.sportvu_elbow_touches_team, conn)
    store_stat(season, season_type, "Player", "PaintTouch", is_regular_season, schema.sportvu_paint_touches, conn)
    store_stat(season, season_type, "Team", "PaintTouch", is_regular_season, schema.sportvu_paint_touches_team, conn)
    store_stat(season, season_type, "Player", "PostTouch", is_regular_season, schema.sportvu_post_touches, conn)
    store_stat(season, season_type, "Team", "PostTouch", is_regular_season, schema.sportvu_post_touches_team, conn)
    store_stat(season, season_type, "Player", "Possessions", is_regular_season, schema.sportvu_possessions, conn)
    store_stat(season, season_type, "Team", "Possessions", is_regular_season, schema.sportvu_possessions_team, conn)

if __name__ == '__main__':
    main()
