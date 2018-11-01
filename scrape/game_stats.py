import json

import helper

class GameData:
    def __init__(self, game_id, season, season_type):
        self.game_id = game_id
        self.season = season
        self.season_type = season_type

        self.pbp_base_url = "http://stats.nba.com/stats/playbyplayv2"
        self.player_tracking_boxscore_base_url = "http://stats.nba.com/stats/boxscoreplayertrackv2"
        self.traditional_boxscore_base_url = "http://stats.nba.com/stats/boxscoretraditionalv2"
        self.advanced_boxscore_base_url = "http://stats.nba.com/stats/boxscoreadvancedv2"
        self.scoring_boxscore_base_url = "http://stats.nba.com/stats/boxscorescoringv2"
        self.misc_boxscore_base_url = "http://stats.nba.com/stats/boxscoremiscv2"
        self.usage_boxscore_base_url = "http://stats.nba.com/stats/boxscoreusagev2"
        self.four_factors_boxscore_base_url = "http://stats.nba.com/stats/boxscorefourfactorsv2"
        self.summary_base_url = "http://stats.nba.com/stats/boxscoresummaryv2"
        self.shots_base_url = "http://stats.nba.com/stats/shotchartdetail"
        self.teams = [self.player_tracking_boxscore_team()[0]['TEAM_ID'], self.player_tracking_boxscore_team()[1]['TEAM_ID']]

    def pbp(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.pbp_base_url, parameters, 0)

    def player_tracking_boxscore(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters(self.player_tracking_boxscore_base_url, parameters, 0)

    def player_tracking_boxscore_team(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters(self.player_tracking_boxscore_base_url, parameters, 1)

    def traditional_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.traditional_boxscore_base_url, parameters, 0)

    def traditional_boxscore_team(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.traditional_boxscore_base_url, parameters, 1)

    def advanced_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.advanced_boxscore_base_url, parameters, 0)

    def advanced_boxscore_team(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.advanced_boxscore_base_url, parameters, 1)

    def scoring_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.scoring_boxscore_base_url, parameters, 0)

    def scoring_boxscore_team(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.scoring_boxscore_base_url, parameters, 1)

    def misc_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.misc_boxscore_base_url, parameters, 0)

    def misc_boxscore_team(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.misc_boxscore_base_url, parameters, 1)

    def usage_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.usage_boxscore_base_url, parameters, 0)

    def four_factors_boxscore(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.four_factors_boxscore_base_url, parameters, 0)

    def four_factors_boxscore_team(self, start_period=0, end_period=10, range_type=2, start_range=0, end_range=55800):
        parameters = {
                        "GameId": self.game_id,
                        "StartPeriod": start_period,
                        "EndPeriod": end_period,
                        "RangeType": range_type,
                        "StartRange": start_range,
                        "EndRange": end_range
        }
        return helper.get_data_from_url_with_parameters(self.four_factors_boxscore_base_url, parameters, 1)

    def shots(self, player_id = 0, outcome="", location="", month=0, season_segment="", date_from="", date_to="", opponent_team_id=0, vs_conference="", vs_division="", position="", game_segment="", rookie_year="", period=0, last_n_games=0, context_measure="FG_PCT"):
        game_shots = []
        for team in self.teams:
            parameters = {
                            "GameID": self.game_id,
                            "Season": self.season,
                            "SeasonType": self.season_type,
                            "TeamID": team,
                            "PlayerID": player_id,
                            "Outcome": outcome,
                            "Location": location,
                            "Month": month,
                            "SeasonSegment": season_segment,
                            "DateFrom": date_from,
                            "DateTo": date_to,
                            "OpponentTeamID": opponent_team_id,
                            "VsConference": vs_conference,
                            "VsDivision": vs_division,
                            "Position": position,
                            "RookieYear": rookie_year,
                            "GameSegment": game_segment,
                            "Period": period,
                            "LastNGames":  last_n_games,
                            "ContextMeasure": context_measure
            }
            game_shots += helper.get_data_from_url_with_parameters(self.shots_base_url, parameters, 0)
        return game_shots

    def game_info(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters_add_game_id(self.summary_base_url, parameters, self.game_id, 4)

    def game_summary(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters(self.summary_base_url, parameters, 0)

    def line_score(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters(self.summary_base_url, parameters, 5)

    def officials(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters_add_game_id(self.summary_base_url, parameters, self.game_id, 2)

    def other_stats(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters_add_game_id(self.summary_base_url, parameters, self.game_id, 1)

    def inactives(self):
        parameters = {"GameId": self.game_id}
        return helper.get_data_from_url_with_parameters_add_game_id(self.summary_base_url, parameters, self.game_id, 3)
