#!/usr/bin/env python3

from flask import Flask, send_from_directory, render_template, Blueprint
import requests, os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('app', __name__)


@bp.route("/")
def main():
    return render_template('index.html',
                           currencies=get_currency_list(),
                           chart_url=get_chart_url(),
                           **get_stats()
                           )


def get_currency_list():
    #return ["USD", "CAD"]
    response = requests.get(os.getenv("ANALYSIS_BASE_URL")+"/currencies")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def get_stats():
    # return {
    #         'current_rate': 1.361598,
    #         'min_rate': 1.361598,
    #         'max_rate': 1.362088,
    #         'mean_rate': (1.361598 + 1.362088)/2
    #         }
    response = requests.get(os.getenv("ANALYSIS_BASE_URL")+"/stats/USD/CAD")
    if response.status_code == 200:
        return response.json()
    else:
        return {}
    
def get_chart_url():
    #return "https://play.teleporthq.io/static/svg/default-img.svg"
    response = requests.get(os.getenv("ANALYSIS_BASE_URL")+"/chart/USD/CAD")
    if response.status_code == 200:
        return response.json()["chart_url"]
    else:
        return {}
    

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp)

    return app

app = create_app()