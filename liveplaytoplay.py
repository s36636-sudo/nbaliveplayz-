
from nba_api.live.nba.endpoints import playbyplay
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.static import teams

import time
import json

nba_teams = teams.get_teams()


selection_input = input('select yout team:')
selection = [team for team in nba_teams if team['abbreviation'] == selection_input][0]
your_teamid = selection['id']
print(f'{selection['full_name']}: {your_teamid}')

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=your_teamid,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)
games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']
game = games[0]
game_id = game['GAME_ID']
n = 0


def request_play():
    pbp = playbyplay.PlayByPlay(game_id)
    line = "{action_number}: {period}:{clock} ({action_type})"
    actions = pbp.get_dict()['game']['actions']
    action = actions[n] 
    action_count = actions[n]['actionNumber']
    player_name = ''
    player = players.find_player_by_id(action['personId'])
    if player is not None:
        player_name = player['full_name']
        # career = playercareerstats.PlayerCareerStats(f'{player['id']}')
        # career.get_dict()[0]
    print(line.format(action_number=action['actionNumber'],period=action['period'],clock=action['clock'],action_type=action['description']))
    

while True:
    try:
       request_play()
       n += 1
       time.sleep(1)
    except IndexError:
        time.sleep(10)
    except json.decoder.JSONDecodeError:
        time.sleep(30)
        print('chuj nie graja jescze')

