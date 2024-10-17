from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap5
import threading
import pytesseract
import cv2
from nhl import *
from mlb import *

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route("/")
def main():
    return render_template("homepage.html")


@app.route("/nhl")
def nhl():
    schedule = getNHLSchedule()
    return render_template("nhl.html", games=schedule)


@app.route("/mlb")
def mlb():
    schedule = getMLBSchedule()
    return render_template("mlb.html", games=schedule)


@app.route("/show")
def show():
    return render_template("show.html", game="show")


@app.route("/display")
def display():
    return render_template("display.html")


prev_score = {
    "home": "0",
    "away": "0",
}

prev_home_run = False

# Hard-coded locations for scorebugs
scorebug_locations = {
    "show": {
        "home": {
            "y_start": 1760 + 110 + 45,
            "y_end": 1760 + 110 + 140,
            "x_start": 2770 + 180,
            "x_end": 2770 + (490 + 180) // 2,
        },
        "away": {
            "y_start": 1760 + 110 + 45,
            "y_end": 1760 + 110 + 140,
            "x_start": 2770 + (490 + 180) // 2,
            "x_end": 2770 + 490,
        },
        "home run": {
            "y_start": 1620,
            "y_end": 1620 + 140,
            "x_start": 2890,
            "x_end": 2890 + 730,
        },
    }
}


def home_score(img, game):
    home_y_start, home_y_end, home_x_start, home_x_end = scorebug_locations[game][
        "home"
    ].values()
    home_score_img = img[home_y_start:home_y_end, home_x_start:home_x_end]
    return pytesseract.image_to_string(
        home_score_img,
        lang="eng",
        config="--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789",
    ).strip()


def away_score(img, game):
    away_y_start, away_y_end, away_x_start, away_x_end = scorebug_locations[game][
        "away"
    ].values()
    away_score_img = img[away_y_start:away_y_end, away_x_start:away_x_end]
    return pytesseract.image_to_string(
        away_score_img,
        lang="eng",
        config="--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789",
    ).strip()


def home_run(img):
    hr_y_start, hr_y_end, hr_x_start, hr_x_end = scorebug_locations["show"][
        "home run"
    ].values()
    home_run = img[hr_y_start:hr_y_end, hr_x_start:hr_x_end]
    return pytesseract.image_to_string(home_run, lang="eng", config=f"--psm 6 --oem 3")


@app.route("/read_frame", methods=["POST"])
def process_frame():
    # Read in current frame and get game type
    img = cv2.imread("static/show1.png")
    game = request.json.get("game")

    # Fetch Home Score
    home_score_txt = home_score(img, game)

    # Fetch Away Score
    away_score_txt = away_score(img, game)

    print(home_score_txt, away_score_txt)

    if home_score_txt != prev_score["home"]:
        if game == "show":
            # Fetch HR status
            home_run_txt = home_run(img)
            print(home_run_txt)
            if home_run_txt == "HOME-RUN" or "HOME RUN":
                print("Away team finish your beer!")
        print("Home Scored!")

    elif away_score_txt != prev_score["away"]:
        if game == "show":
            # Fetch HR status
            home_run_txt = home_run(img)
            if home_run_txt == "HOME-RUN" or "HOME RUN":
                print("Home team finish your beer!")
        print("Away Scored!")

    prev_score["home"], prev_score["away"] = home_score, away_score

    return jsonify({"status": "Frame reading initiated"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=4996)
