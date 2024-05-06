from pydub import AudioSegment
from pydub.playback import play
import requests
import time


url = 'https://api-web.nhle.com/v1/gamecenter/2023030157/boxscore'

dallas_goal = AudioSegment.from_mp3('static/nhl_goal/DAL_goal.mp3')
vegas_goal = AudioSegment.from_mp3('static/nhl_goal/VGK_goal.mp3')

def main():
    game_state = 'LIVE'
    old_away_score = 1
    old_home_score = 2
    while game_state == 'LIVE' or game_state == 'CRIT':
        game = requests.get(url).json()
        game_state = game['gameState']
        current_away_score = game['awayTeam']['score']
        current_home_score = game['homeTeam']['score']
        if (current_away_score == old_away_score + 1):
            time.sleep(10)
            play(vegas_goal)
        if (current_home_score == old_home_score + 1):
            time.sleep(10)
            play(dallas_goal)
        old_away_score = current_away_score
        old_home_score = current_home_score
        time.sleep(2)
    if (current_away_score > current_home_score):
        play(vegas_goal)
    elif (current_home_score > current_away_score):
        play(dallas_goal)
    print(f'VGK {current_away_score}')
    print(f'DAL {current_home_score}')


if __name__=='__main__':
    main()