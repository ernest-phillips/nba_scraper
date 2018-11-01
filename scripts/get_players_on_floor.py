import json
import logging
from sqlalchemy import create_engine, distinct
from sqlalchemy.sql import select
from pandas import DataFrame

from process import pbp
from storage import schema
from utils import utils

def main():
    logging.basicConfig(filename='logs/process_pbp.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config=json.loads(open('config.json').read())

    # connect to database
    username = config['username']
    password = config['password']
    host = config['host']
    database = config['database']

    engine = create_engine('mysql://'+username+':'+password+'@'+host+'/'+database)
    conn = engine.connect()

    # get game_ids to process
    games_to_process = []
    missing_games_query = select([distinct(schema.pbp.c.GAME_ID)]).where(schema.pbp.c.HOME_PLAYER1 == None)
    for game in conn.execute(missing_games_query):
        games_to_process.append(game.GAME_ID)

    # add players on floor to database
    for game_id in games_to_process:
        try:
            pbp_query = select([(schema.pbp)]).where(schema.pbp.c.GAME_ID == game_id)
            results = conn.execute(pbp_query)
            pbp_data = DataFrame(results.fetchall())
            pbp_data.columns = results.keys()

            game_data = pbp.Lineups(pbp_data)
            pbp_with_lineups =  game_data.get_players_on_floor_for_game()
            conn.execute(schema.pbp.insert(replace_string=""), pbp_with_lineups)
        except:
            logging.error(utils.LogException())


if __name__ == '__main__':
    main()
