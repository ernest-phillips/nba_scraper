import json
import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36"
REFERER = "http://stats.nba.com/scores/"

def get_data_from_url_with_parameters(base_url, parameters, index):
    response = requests.get(base_url, params=parameters, headers={'User-Agent': USER_AGENT, 'referer': REFERER})
    data = response.json()
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, row)) for row in rows]

def get_data_from_url_with_parameters_add_game_id(base_url, parameters, game_id, index):
    response = requests.get(base_url, params=parameters, headers={'User-Agent': USER_AGENT, 'referer': REFERER})
    data = response.json()
    headers = data['resultSets'][index]['headers']
    headers = ["GAME_ID"] + headers
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, [game_id] + row)) for row in rows]

def get_data_from_url_with_parameters_add_player_id(base_url, parameters, player_id, player_name, index):
    response = requests.get(base_url, params=parameters, headers={'User-Agent': USER_AGENT, 'referer': REFERER})
    data = response.json()
    headers = data['resultSets'][index]['headers']
    headers = ["PLAYER_ID", "PLAYER_NAME"] + headers
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, [player_id, player_name] + row)) for row in rows]

def get_data_from_url(url, index):
    response = requests.get(url, headers={ 'User-Agent': USER_AGENT })
    data = response.json()
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, row)) for row in rows]

def get_data_from_url_add_player_id(url, player_id, player_name, index):
    response = requests.get(url, headers={ 'User-Agent': USER_AGENT })
    data = response.json()
    headers = data['resultSets'][index]['headers']
    headers = ["PLAYER_ID", "PLAYER_NAME"] + headers
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, [player_id, player_name] + row)) for row in rows]

def get_data_from_url_add_game_id(url, game_id, index):
    response = requests.get(url, headers={ 'User-Agent': USER_AGENT })
    data = response.json()
    headers = data['resultSets'][index]['headers']
    headers = ["GAME_ID"] + headers
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, [game_id] + row)) for row in rows]

def get_data_from_url_rename_columns(url, renamed_columns, index):
    response = requests.get(url, headers={ 'User-Agent': USER_AGENT })
    data = response.json()
    headers = data['resultSets'][index]['headers']
    for key in renamed_columns.keys():
        headers = [renamed_columns[key] if x==key else x for x in headers]
    rows = data['resultSets'][index]['rowSet']
    return [dict(zip(headers, row)) for row in rows]

def get_game_ids_for_date(date):
    # date format YYYY-MM-DD
    game_ids = []
    split = date.split("-")
    parameters = {
                    "DayOffset": 0,
                    "LeagueID": "00",
                    "gameDate": split[1]+"/"+split[2]+"/"+split[0]
    }
    games = get_data_from_url_with_parameters("http://stats.nba.com/stats/scoreboardV2", parameters, 1)
    for game in games:
        game_ids.append(game['GAME_ID'])
    return list(set(game_ids))
