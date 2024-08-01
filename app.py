from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from nhl import *
from mlb import *
import time
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)

current_away_score = 0
current_home_score = 0


@app.route('/')
def main():
    return render_template('homepage.html')

@app.route('/nhl')
def nhl():
    schedule = getNHLSchedule()
    return render_template('nhl.html', games=schedule)

@app.route('/mlb')
def mlb():
    schedule = getMLBSchedule()
    return render_template('mlb.html', games=schedule)

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/watch')
def watch():
    global current_away_score
    global current_home_score

    league = request.args.get('league')
    game_id = request.args.get('gameID')

    # check if the continue flag is set within the url. If it is, do not initialize the score.

    cont = request.args.get('continue')

    if(not cont):
        current_away_score, current_home_score = getNHLScore(game_id)

    # check the toggles for away and home teams
    awayon = request.args.get('awayTeam')
    if (awayon == None): awayon = 1
    
    homeon = request.args.get('homeTeam')
    if (homeon == None): homeon = 1

    delay = request.args.get('delay')
    if (delay == None): delay = 0

    if (league == 'nhl'):
        data = getNHLGameInfo(game_id, current_away_score, current_home_score)

        current_away_score = data['game_info']['away_score']
        current_home_score = data['game_info']['home_score']

        data['awayTeam'] = True if (int(awayon) == 1) else False
        data['homeTeam'] = True if (int(homeon) == 1) else False
        data['delay'] = int(delay)

        if (data['goal'] != 'none' or data['game_info']['game_state'] == 'FINAL' or data['game_info']['game_state'] == 'OFF'):
            setMonitor()
            while (True):
                live_time = getTimestamp()
                print("game time: ", data['game_info']['clock'])
                print("Timestamp: ", live_time)
                if (live_time is not None and live_time == getSecondsAPI(data['game_info']['clock'])):
                    break
                time.sleep(1)
        
        # TODO shorten goal audio, remove delay slider, fix win animation

    return render_template('watch.html', data=data)

def getSecondsAPI(time: str) -> int:
    pattern = re.compile(r'\d+')
    matches = re.findall(pattern, time)

    return int(matches[0]) * 60 + int(matches[1])

if __name__=='__main__':
    app.run(debug=True, port=4996)