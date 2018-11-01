import json

import helper

def get_sportvu_data_for_stat(season, season_type, player_or_team, measure_type, start_date="", end_date="", last_n_games=0, league_id="00", month=0, opponent_team_id=0, por_round=0, per_mode="Totals", team_id=0, outcome="", location="", season_segment="", vs_conference="", vs_division="", game_scope="", player_experience="", player_position="", starter_bench=""):
    parameters = {
                    "DateFrom": start_date,
                    "DateTo": end_date,
                    "PlayerOrTeam": player_or_team,
                    "PtMeasureType": measure_type,
                    "Season": season,
                    "SeasonType": season_type,
                    "LastNGames": last_n_games,
                    "LeagueID": league_id,
                    "Month": month,
                    "OpponentTeamID": opponent_team_id,
                    "PORound": por_round,
                    "PerMode": per_mode,
                    "TeamID": team_id,
                    "Outcome": outcome,
                    "Location": location,
                    "SeasonSegment": season_segment,
                    "VsConference": vs_conference,
                    "VsDivision": vs_division,
                    "GameScope": game_scope,
                    "PlayerExperience": player_experience,
                    "PlayerPosition": player_position,
                    "StarterBench": starter_bench
    }
    base_url = "http://stats.nba.com/stats/leaguedashptstats"
    return helper.get_data_from_url_with_parameters(base_url, parameters, 0)

def add_game_id_to_game_log_for_player(daily_data, date, game_ids, player_game_map):
    to_return = []
    for row in daily_data:
        player_id = str(row["PLAYER_ID"])
        for game_id in game_ids:
            if game_id in player_game_map[player_id].keys():
                row[u'GAME_ID'] = game_id
                row[u'TEAM_ID'] = player_game_map[player_id][game_id]
                to_return.append(row)
                break
    return to_return

def add_game_id_to_game_log_for_team(daily_data, date, game_ids, team_game_map):
    to_return = []
    for row in daily_data:
        team_id = str(row["TEAM_ID"])
        for game_id in game_ids:
            if game_id in team_game_map[team_id].keys():
                row[u'GAME_ID'] = game_id
                to_return.append(row)
                break
    return to_return
