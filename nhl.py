from datetime import date, datetime
import pytz
import requests
import shutil
import os

date_format = '%Y-%m-%d %H:%M:%S'
local_timezone = pytz.timezone('America/New_York')
la_timezone = pytz.timezone('America/Los_Angeles')


def getNHLSchedule():
    schedule_return = []
    today = local_timezone.localize(datetime.now()).astimezone(la_timezone).strftime('%Y-%m-%d')
    url = 'https://api-web.nhle.com/v1/schedule/' + str(today)
    schedule = requests.get(url).json()['gameWeek'][0]['games']
    for game in schedule:
        g = {}
        away_team = game['awayTeam']['abbrev']
        home_team = game['homeTeam']['abbrev']
        getLogo(game['awayTeam']['logo'])
        getLogo(game['homeTeam']['logo'])
        away_logo = 'static/nhl/' + game['awayTeam']['logo'].split('/')[-1]
        home_logo = 'static/nhl/' + game['homeTeam']['logo'].split('/')[-1]
        game_state = game['gameState']
        if (game_state == 'FUT' or game_state == 'PRE'):
            start = game['startTimeUTC'].split('T')
            start_time = start[0] + ' ' + start[1].split('Z')[0]
            date_obj = datetime.strptime(start_time, date_format).replace(tzinfo=pytz.UTC).astimezone(local_timezone).strftime('%B %d, %Y %I:%M %p')
            
            g = dict({'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'time': date_obj, 'game_state': game_state})
        elif (game_state == 'OFF' or game_state == 'FINAL'):
            away_score = game['awayTeam']['score']
            home_score = game['homeTeam']['score']
            
            g = dict({'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'away_score': away_score, 'home_score': home_score, 'game_state': game_state})

        else:
            away_score = game['awayTeam']['score']
            home_score = game['homeTeam']['score']

            period = game['periodDescriptor']['number']
            
            g = dict({'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'away_score': away_score, 'home_score': home_score, 'game_state': game_state, 'period': period})


        schedule_return.append(g)
    return schedule_return
        
def getLogo(url):
    file_name = 'static/nhl/' + url.split('/')[-1]
    if (not os.path.exists(file_name)):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'w') as f:
                f.write(r.text)
    

def main():
    getNHLSchedule()

if __name__=='__main__':
    main()