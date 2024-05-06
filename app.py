from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from nhl import *
from mlb import *

app = Flask(__name__)
bootstrap = Bootstrap5(app)


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

if __name__=='__main__':
    app.run(debug=True, port=4996)