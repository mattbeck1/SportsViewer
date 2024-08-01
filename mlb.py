from datetime import date, datetime
import pytz
import requests
import shutil
import os
from send_requests import send_get_request

date_format = '%Y-%m-%d %H:%M:%S'
local_timezone = pytz.timezone('America/New_York')
la_timezone = pytz.timezone('America/Los_Angeles')

team_abbrev = {}

def getMLBSchedule():
    schedule_return = []
    today = local_timezone.localize(datetime.now()).astimezone(la_timezone).strftime('%Y-%m-%d')
    url = f'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={today}&endDate={today}'
    schedule = requests.get(url).json()['dates'][0]['games']
    for game in schedule:
        g = {}
        away_name = game['teams']['away']['team']['name']
        home_name = game['teams']['home']['team']['name']

        try:
            away_team = team_abbrev[away_name]
        except:
            away_url = 'http://statsapi.mlb.com' + game['teams']['away']['team']['link']
            away_team = getTeamAbbrev(away_name, away_url)

        try:
            home_team = team_abbrev[home_name]
        except:
            home_url = 'http://statsapi.mlb.com' + game['teams']['home']['team']['link']
            home_team = getTeamAbbrev(home_name, home_url)

        away_logo = f'static/mlb/{away_team}_logo.svg'
        home_logo = f'static/mlb/{home_team}_logo.svg'

        game_state = game['status']['codedGameState']
        game_id = game['gamePk']

        if (game_state == 'S' or game_state == 'P'):
            start = game['gameDate'].split('T')
            start_time = start[0] + ' ' + start[1].split('Z')[0]
            date_obj = datetime.strptime(start_time, date_format).replace(tzinfo=pytz.UTC).astimezone(local_timezone).strftime('%B %d, %Y %I:%M %p')

            g = dict({'away_team': away_team, 'home_team': home_team, 'time': date_obj, 'away_logo': away_logo, 'home_logo': home_logo, 'game_state': game_state})

        elif (game_state == 'I'):
            away_score = game['teams']['away']['score']
            home_score = game['teams']['home']['score']

            g = dict({'game_id':game_id, 'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'away_score': away_score, 'home_score': home_score, 'game_state': game_state})
        
        elif (game_state == 'F'):
            away_score = game['teams']['away']['score']
            home_score = game['teams']['home']['score']

            g = dict({'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'away_score': away_score, 'home_score': home_score, 'game_state': game_state})
        
        schedule_return.append(g)
        print(g)
    return schedule_return
        
def getTeamAbbrev(name, url):
    team_details = requests.get(url).json()
    abbrev = team_details['teams'][0]['abbreviation']
    team_abbrev[name] = abbrev
    return abbrev

def getMLBGameInfo(gameID:int, current_away_score:int, current_home_score:int) -> dict():
    url = f'http://statsapi.mlb.com/api/v1/game/{gameID}/content'
    return_request = send_get_request(url)
    game_data = return_request.json()



def main():
    getMLBSchedule()

if __name__=='__main__':
    main()