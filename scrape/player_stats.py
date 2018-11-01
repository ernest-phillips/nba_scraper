import json

import helper

class PlayerData:
    def __init__(self, player_id, player_name, season, season_type):
        self.player_id = player_id
        self.player_name = player_name
        self.season = season
        self.season_type = season_type

        self.player_tracking_shot_logs_base_url = "http://stats.nba.com/stats/playerdashptshotlog"
        self.player_tracking_rebound_logs_base_url = "http://stats.nba.com/stats/playerdashptreboundlogs"
        self.player_tracking_passes_base_url = "http://stats.nba.com/stats/playerdashptpass"

    def shot_logs(self, league_id="00", team_id=0, outcome="", location="", month=0, season_segment="", date_from="", date_to="", opponent_team_id=0, vs_conference="", vs_division="", game_segment="", period=0, last_n_games=0):
        parameters = {
                        "LeagueID": league_id,
                        "Season": self.season,
                        "SeasonType": self.season_type,
                        "PlayerID": self.player_id,
                        "TeamID": team_id,
                        "Outcome": outcome,
                        "Location": location,
                        "Month": month,
                        "SeasonSegment": season_segment,
                        "DateFrom": date_from,
                        "DateTo": date_to,
                        "OpponentTeamID": opponent_team_id,
                        "VsConference": vs_conference,
                        "VsDivision": vs_division,
                        "GameSegment": game_segment,
                        "Period": period,
                        "LastNGames": last_n_games
        }
        return helper.get_data_from_url_with_parameters_add_player_id(self.player_tracking_shot_logs_base_url, parameters, self.player_id, self.player_name, 0)

    def rebound_logs(self, league_id="00", team_id=0, outcome="", location="", month=0, season_segment="", date_from="", date_to="", opponent_team_id=0, vs_conference="", vs_division="", game_segment="", period=0, last_n_games=0):
        parameters = {
                        "LeagueID": league_id,
                        "Season": self.season,
                        "SeasonType": self.season_type,
                        "PlayerID": self.player_id,
                        "TeamID": team_id,
                        "Outcome": outcome,
                        "Location": location,
                        "Month": month,
                        "SeasonSegment": season_segment,
                        "DateFrom": date_from,
                        "DateTo": date_to,
                        "OpponentTeamID": opponent_team_id,
                        "VsConference": vs_conference,
                        "VsDivision": vs_division,
                        "GameSegment": game_segment,
                        "Period": period,
                        "LastNGames": last_n_games
        }
        return helper.get_data_from_url_with_parameters_add_player_id(self.player_tracking_rebound_logs_base_url, parameters, self.player_id, self.player_name, 0)

    def passes_made(self, league_id="00", team_id=0, outcome="", location="", month=0, season_segment="", date_from="", date_to="", opponent_team_id=0, vs_conference="", vs_division="", game_segment="", period=0, last_n_games=0, per_mode="Totals"):
        parameters = {
                        "LeagueID": league_id,
                        "Season": self.season,
                        "SeasonType": self.season_type,
                        "PlayerID": self.player_id,
                        "TeamID": team_id,
                        "Outcome": outcome,
                        "Location": location,
                        "Month": month,
                        "SeasonSegment": season_segment,
                        "DateFrom": date_from,
                        "DateTo": date_to,
                        "OpponentTeamID": opponent_team_id,
                        "VsConference": vs_conference,
                        "VsDivision": vs_division,
                        "GameSegment": game_segment,
                        "Period": period,
                        "LastNGames": last_n_games,
                        "PerMode": per_mode
        }
        return helper.get_data_from_url_with_parameters(self.player_tracking_passes_base_url, parameters, 0)

    def passes_received(self, league_id="00", team_id=0, outcome="", location="", month=0, season_segment="", date_from="", date_to="", opponent_team_id=0, vs_conference="", vs_division="", game_segment="", period=0, last_n_games=0, per_mode="Totals"):
        parameters = {
                        "LeagueID": league_id,
                        "Season": self.season,
                        "SeasonType": self.season_type,
                        "PlayerID": self.player_id,
                        "TeamID": team_id,
                        "Outcome": outcome,
                        "Location": location,
                        "Month": month,
                        "SeasonSegment": season_segment,
                        "DateFrom": date_from,
                        "DateTo": date_to,
                        "OpponentTeamID": opponent_team_id,
                        "VsConference": vs_conference,
                        "VsDivision": vs_division,
                        "GameSegment": game_segment,
                        "Period": period,
                        "LastNGames": last_n_games,
                        "PerMode": per_mode
        }
        return helper.get_data_from_url_with_parameters(self.player_tracking_passes_base_url, parameters, 1)
