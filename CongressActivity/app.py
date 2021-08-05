from flask import Flask, render_template, request, abort
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

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

def get_legislator_data(api_url):
    data = requests.get(
        api_url,
        headers={"X-API-Key": PROPUBLICA_API_KEY},
    ).json()["results"][0]

    if "youtube_account" in data and data["youtube_account"] is not None:
        twitter = requests.get(f"https://www.youtube.com/user/{data['youtube_account']}")
        soup = BeautifulSoup(twitter.content)
        data["image"] = soup.find("meta", property="og:image").attrs["content"]

    return data



legislators = CONGRESS_DATA["results"][0]["members"] + SENATE_DATA["results"][0]["members"]


@app.route("/")
def home():
    return render_template(
        "pages/home.html",
        legislators=legislators
    )

@app.route("/official")
def official():
    official = request.args.get("official")
    matched_official = list(filter(lambda k: (k["first_name"] + " " + k["last_name"] in official), legislators))

    if len(matched_official) == 0:
        abort(404)

    matched_official = matched_official[0]
    detailed_data = get_legislator_data(matched_official["api_uri"])
    print(detailed_data)

    print(matched_official)

    return render_template(
        "pages/official.html",
         official=matched_official,
         legislators=legislators,
         detailed_data=detailed_data
    )

app.run(debug=True)