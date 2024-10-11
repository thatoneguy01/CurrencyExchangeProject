from flask import Flask, request, Blueprint
from sqlalchemy import desc
from datetime import datetime
from model import ExchangeRates
from quickchart import QuickChart

bp = Blueprint('analysis', __name__)


def get_rate(rates, curr):
    if curr == 'USD':
        return 1
    return getattr(rates, curr)

@bp.route('/currencies')
def get_currencies():
    column_names = list(ExchangeRates.query.all()[0].__dict__.keys())
    column_names.append('USD')
    column_names.remove('_sa_instance_state')
    column_names.remove('datetime')
    column_names.sort()
    return column_names

@bp.route('/convert', methods=["POST"])
def convert():
    data = request.get_json()
    amount = data["amount"]
    curr_source = data["curr_source"]
    curr_result = data["curr_result"]
    current_rates = ExchangeRates.query.filter().order_by(desc(ExchangeRates.datetime)).first()
    conversion_rate = get_rate(current_rates, curr_result) / get_rate(current_rates, curr_source)
    conversion_result = amount * conversion_rate
    return {"source_currency": curr_source,
            "result_currency": curr_result,
            "exchange_rate": conversion_rate,
            "converted_amount": conversion_result}

@bp.route('/stats/<base_currency>/<compare_currency>')
def statistics(base_currency, compare_currency):
    start_date_str = request.args.get('start_date', '')
    try:
        start_date = datetime.fromisoformat(start_date_str)
    except ValueError:
        start_date = datetime.fromtimestamp(946713600)

    current_rates = ExchangeRates.query.filter().order_by(desc(ExchangeRates.datetime)).first()
    conversion_rate = get_rate(current_rates, compare_currency) / get_rate(current_rates, base_currency)
    rates = ExchangeRates.query.where(ExchangeRates.datetime > start_date).all()
    conversion_rates = [get_rate(rate, compare_currency)/get_rate(rate, base_currency) for rate in rates]
    min_rate = min(conversion_rates)
    maz_rate = max(conversion_rates)
    average_rate = sum(conversion_rates) / len(conversion_rates)
    return {'current_rate': conversion_rate,
            'min_rate': min_rate,
            'max_rate': maz_rate,
            'mean_rate': average_rate}

@bp.route('/chart/<base_currency>/<compare_currency>')
def chart(base_currency, compare_currency):
    width = request.args.get('width', 500)
    height = request.args.get('height', 300)
    start_date_str = request.args.get('key', '')
    try:
        start_date = datetime.fromisoformat(start_date_str)
    except ValueError:
        start_date = datetime.fromtimestamp(946713600)

    rates = ExchangeRates.query.where(ExchangeRates.datetime > start_date).all()
    conversion_rates = [get_rate(rate, base_currency)/get_rate(rate, compare_currency) for rate in rates]

    qc = QuickChart()
    qc.width = width
    qc.height = height
    qc.version = '2.9.4'
    qc.config = {
                    'type': 'line',
                     'data': {
                        'labels': ['']*len(conversion_rates),
                        'datasets': [
                            {
                                'label': f'{base_currency} to {compare_currency} Exchange Rate',
                                'cubicInterpolationMode': False,
                                'data': conversion_rates,
                                'fill': False,
                                'borderColor': 'green',
                            },
                        ],
                    },
    }
    return {"chart_url": qc.get_url()}

def create_app(db_path = 'sqlite:///ExchangeRates.sqlite3'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path

    app.register_blueprint(bp)

    from model import db
    db.init_app(app)
    
    return app

app = create_app()