from datetime import date, datetime
import pytz
import requests
import os
import numpy as np
import pytesseract
import mss
import cv2 as cv
from matplotlib import pyplot as plt
import re
import time
from send_requests import send_get_request

date_format = '%Y-%m-%d %H:%M:%S'
local_timezone = pytz.timezone('America/New_York')
la_timezone = pytz.timezone('America/Los_Angeles')
monitor = None
minute_pattern = re.compile(r'\d{1,2}:\d{2}')
second_pattern = re.compile(r'\d{1,2}.\d')


def getNHLSchedule():
    schedule_return = []
    today = local_timezone.localize(datetime.now()).astimezone(la_timezone).strftime('%Y-%m-%d')
    url = 'https://api-web.nhle.com/v1/schedule/' + str(today)
    schedule = requests.get(url).json()['gameWeek'][0]['games']
    for game in schedule:
        g = {}

        game_id = game['id']

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
            
            g = dict({'game_id': game_id, 'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'away_score': away_score, 'home_score': home_score, 'game_state': game_state, 'period': period})


        schedule_return.append(g)
    return schedule_return
        
def getLogo(url):
    file_name = 'static/nhl/' + url.split('/')[-1]
    if (not os.path.exists(file_name)):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'w') as f:
                f.write(r.text)

def getNHLGameInfo(gameID:int, current_away_score: int, current_home_score: int):
    url = f'https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore'
    return_request = send_get_request(url)
    game_data = return_request.json()
    # game_data = requests.get(url).json()

    away_team = game_data['awayTeam']['abbrev']
    home_team = game_data['homeTeam']['abbrev']
    
    away_logo = 'static/nhl/' + game_data['awayTeam']['logo'].split('/')[-1]
    home_logo = 'static/nhl/' + game_data['homeTeam']['logo'].split('/')[-1]
    game_state = game_data['gameState']

    away_score = game_data['awayTeam']['score']

    home_score = game_data['homeTeam']['score']

    period = game_data['periodDescriptor']['number']
    clock = game_data['clock']['timeRemaining']
    intermission = game_data['clock']['inIntermission']
    clock_running = game_data['clock']['running']

    game_info = {'league': 'nhl', 'away_team': away_team, 'home_team': home_team, 'away_logo': away_logo, 'home_logo': home_logo, 'game_state': game_state, 'away_score': away_score, 'home_score': home_score, 'period': period, 'clock': clock, 'intermission': intermission, 'clock_running': clock_running }

    away_box_data = game_data['playerByGameStats']['awayTeam']
    home_box_data = game_data['playerByGameStats']['homeTeam']

    team_data = game_data['summary']['teamGameStats']

    away_sog = team_data[0]['awayValue']
    home_sog = team_data[0]['homeValue']
    
    away_fopct = team_data[1]['awayValue']
    home_fopct = team_data[1]['homeValue']

    away_pp = team_data[2]['awayValue']
    home_pp = team_data[2]['homeValue']

    away_pim = team_data[4]['awayValue']
    home_pim = team_data[4]['homeValue']

    away_hits = team_data[5]['awayValue']
    home_hits = team_data[5]['homeValue']

    away_bs = team_data[6]['awayValue']
    home_bs = team_data[6]['homeValue']

    away_ga = team_data[7]['awayValue']
    home_ga = team_data[7]['homeValue']

    away_ta = team_data[8]['awayValue']
    home_ta = team_data[8]['homeValue']

    away_info = {'sog': away_sog, 'fopct': away_fopct, 'pp': away_pp, 'pim': away_pim, 'hits': away_hits, 'bs': away_bs, 'ga': away_ga, 'ta': away_ta}
    home_info = {'sog': home_sog, 'fopct': home_fopct, 'pp': home_pp, 'pim': home_pim, 'hits': home_hits, 'bs': home_bs, 'ga': home_ga, 'ta': home_ta}

    away_forwards = []

    for f in away_box_data['forwards']:
        name = f['name']['default']
        number = f['sweaterNumber']
        position = f['position']
        goals = f['goals']
        assists = f['assists']
        points = f['points']
        plusMinus = f['plusMinus']
        try:
            pim = f['pim']
        except:
            pim = 0
        hits = f['hits']
        ppg = f['powerPlayGoals']
        shots = f['shots']
        faceoff = f['faceoffWinningPctg']
        try:
            toi = f['toi']
        except:
            toi = 0
        away_forward = {'name': name, 'number': number, 'position': position, 'goals': goals, 'assists': assists, 'points': points, 'plusMinus': plusMinus, 'pim': pim, 'hits': hits, 'ppg': ppg, 'shots': shots, 'faceoff': faceoff, 'toi':toi}
        away_forwards.append(away_forward)

    away_defencemen = []
    
    for d in away_box_data['defense']:
        name = d['name']['default']
        number = d['sweaterNumber']
        position = d['position']
        goals = d['goals']
        assists = d['assists']
        points = d['points']
        plusMinus = d['plusMinus']
        try:
            pim = d['pim']
        except:
            pim = 0
        hits = d['hits']
        ppg = d['powerPlayGoals']
        shots = d['shots']
        faceoff = d['faceoffWinningPctg']
        try:
            toi = d['toi']
        except:
            toi = 0
        away_defenseman = {'name': name, 'number': number, 'position': position, 'goals': goals, 'assists': assists, 'points': points, 'plusMinus': plusMinus, 'pim': pim, 'hits': hits, 'ppg': ppg, 'shots': shots, 'faceoff': faceoff, 'toi':toi}
        away_defencemen.append(away_defenseman)
    
    away_goalies = []

    for g in away_box_data['goalies']:
        name = g['name']['default']
        number = g['sweaterNumber']
        position = g['position']
        ppsa = g['powerPlayShotsAgainst']
        shsa = g['shorthandedShotsAgainst']
        sa = g['saveShotsAgainst']
        try:
            svpct = g['savePctg']
        except:
            svpct = 0
        ppga = g['powerPlayGoalsAgainst']
        shga = g['shorthandedGoalsAgainst']
        try:
            pim = g['pim']
        except:
            pim = 0
        ga = g['goalsAgainst']
        try:
            toi = g['toi']
        except:
            toi = 0
        try:
            starter = g['starter']
        except:
            starter = False
        away_goalie = {'name': name, 'number': number, 'position': position, 'ppsa': ppsa, 'shsa': shsa, 'sa': sa, 'svpct': svpct, 'ppga': ppga, 'shga': shga, 'pim': pim, 'ga': ga, 'toi': toi, 'starter': starter }
        away_goalies.append(away_goalie)

    away_box = {'forwards': away_forwards, 'defencemen': away_defencemen, 'goalies': away_goalies}

    home_forwards = []

    for f in home_box_data['forwards']:
        name = f['name']['default']
        number = f['sweaterNumber']
        position = f['position']
        goals = f['goals']
        assists = f['assists']
        points = f['points']
        plusMinus = f['plusMinus']
        try:
            pim = f['pim']
        except:
            pim = 0
        hits = f['hits']
        ppg = f['powerPlayGoals']
        shots = f['shots']
        faceoff = f['faceoffWinningPctg']
        try:
            toi = f['toi']
        except:
            toi = 0
        home_forward = {'name': name, 'number': number, 'position': position, 'goals': goals, 'assists': assists, 'points': points, 'plusMinus': plusMinus, 'pim': pim, 'hits': hits, 'ppg': ppg, 'shots': shots, 'faceoff': faceoff, 'toi':toi}
        home_forwards.append(home_forward)

    home_defencemen = []
    
    for d in home_box_data['defense']:
        name = d['name']['default']
        number = d['sweaterNumber']
        position = d['position']
        goals = d['goals']
        assists = d['assists']
        points = d['points']
        plusMinus = d['plusMinus']
        try:
            pim = d['pim']
        except:
            pim = 0
        hits = d['hits']
        ppg = d['powerPlayGoals']
        shots = d['shots']
        faceoff = d['faceoffWinningPctg']
        try:
            toi = d['toi']
        except:
            toi = 0
        home_defenseman = {'name': name, 'number': number, 'position': position, 'goals': goals, 'assists': assists, 'points': points, 'plusMinus': plusMinus, 'pim': pim, 'hits': hits, 'ppg': ppg, 'shots': shots, 'faceoff': faceoff, 'toi':toi}
        home_defencemen.append(home_defenseman)

    home_goalies = []

    for g in home_box_data['goalies']:
        name = g['name']['default']
        number = g['sweaterNumber']
        position = g['position']
        ppsa = g['powerPlayShotsAgainst']
        shsa = g['shorthandedShotsAgainst']
        sa = g['saveShotsAgainst']
        try:
            svpct = g['savePctg']
        except:
            svpct = 0
        ppga = g['powerPlayGoalsAgainst']
        shga = g['shorthandedGoalsAgainst']
        try:
            pim = g['pim']
        except:
            pim = 0
        ga = g['goalsAgainst']
        try:
            toi = g['toi']
        except:
            toi = 0
        try:
            starter = g['starter']
        except:
            starter = False
        home_goalie = {'name': name, 'number': number, 'position': position, 'ppsa': ppsa, 'shsa': shsa, 'sa': sa, 'svpct': svpct, 'ppga': ppga, 'shga': shga, 'pim': pim, 'ga': ga, 'toi': toi, 'starter': starter }
        home_goalies.append(home_goalie)


    home_box = {'forwards': home_forwards, 'defencemen': home_defencemen, 'goalies': home_goalies}

    goal = 'none'

    if (away_score == current_away_score + 1):
        goal = 'away'
    elif (home_score == current_home_score + 1):
        goal = 'home'

    
    return {'game_info': game_info, 'away_info': away_info, 'home_info': home_info, 'away_box': away_box, 'home_box': home_box, 'goal': goal}

def getNHLScore(gameID):
    url = f'https://api-web.nhle.com/v1/gamecenter/{gameID}/boxscore'
    game_data = requests.get(url).json()

    away_score = game_data['awayTeam']['score']

    home_score = game_data['homeTeam']['score']

    return (away_score, home_score)

def setMonitor():
    with mss.mss() as sct:
        global monitor
        monitor_number = 2
        mon = sct.monitors[monitor_number]

        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }


def getTimestamp():
    
    with mss.mss() as sct:
        
        sct_img = sct.grab(monitor)
        img = np.array(sct_img) # BGR Image

        # image = cv.rectangle(image, (410, 95), (495, 135), (250,0,0), 2)

        # fixed location of espn's scoreboard
        scoreboard = img[115:160, 150:245]

        # tnt scoreboard
        # scoreboard = img[95:135, 410:495]

        # scoreboard = image[200:240, 100:168]

        # cv.imshow('Image', scoreboard)
        # cv.waitKey(0)
        # return None
        
        return readTime(scoreboard)


def readTime(scoreboard) -> int:

    custom_config = r'--oem 3 --psm 6'
    time = pytesseract.image_to_string(scoreboard, config=custom_config)
    print(time)
    return getSeconds(time)

def getSeconds(time: str) -> int:
    seconds = None

    if(re.search(minute_pattern, time)):
        pattern = re.compile('\d+')
        matches = re.findall(pattern, time)

        seconds = int(matches[0]) * 60 + int(matches[1])
    
    elif(re.search(second_pattern, time)):
        pattern = re.compile('\d+')
        matches = re.search(pattern, time)

        seconds = int(matches[0])

    return seconds




def main():
    setMonitor()
    getTimestamp()

if __name__=='__main__':
    main()