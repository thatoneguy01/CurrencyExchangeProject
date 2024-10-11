#!/usr/bin/env python3
import requests, os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
sys.path.append("../FinalProject")
from model import db, ExchangeRates
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ExchangeRates.sqlite3'

    db.init_app(app)
    
    return app

app = create_app()

'''
Helper function to get temperature
using API
'''

def get_exchange_rates():
    url = f"https://openexchangerates.org/api/latest.json?app_id={os.getenv('APP_ID')}"
    response = requests.get(url)
    return response.json()["rates"]

def main():
    current_rates = get_exchange_rates()
    new_entry = ExchangeRates(**current_rates)
    with app.app_context():
        db.session.add(new_entry)
        db.session.commit()
'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
if __name__ == "__main__":
    main()