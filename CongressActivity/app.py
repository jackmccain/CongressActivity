from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

PROPUBLICA_API_KEY = os.getenv("PROPUBLICA_API_KEY")

CONGRESS_DATA = requests.get(
    "https://api.propublica.org/congress/v1/117/house/members.json",
    headers={"X-API-Key": PROPUBLICA_API_KEY},
).json()

SENATE_DATA = requests.get(
    "https://api.propublica.org/congress/v1/117/senate/members.json",
    headers={"X-API-Key": PROPUBLICA_API_KEY},
).json()




legislators = CONGRESS_DATA["results"][0]["members"] + SENATE_DATA["results"][0]["members"]


@app.route("/")
def home():
    return render_template(
        "pages/home.html",
    )

@app.route("/official")
def official():
    officials = request.args.getlist("official")

    matched_officials = filter(lambda k: (k["first_name"] + " " + k["last_name"] in officials), legislators)

    return render_template(
        "pages/official.html",
         officials=matched_officials
    )

app.run(debug=True)