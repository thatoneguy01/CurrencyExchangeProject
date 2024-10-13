import pytest
from analysis.analyse import create_app

@pytest.fixture()
def app(mocker):
    mocker.patch('quickchart.QuickChart.get_url', return_value="http://www.testchart.com")
    mocker.patch('flask_monitoringdashboard.bind', return_value=None)
    app = create_app('sqlite:///ExchangeRates_test.sqlite3')
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


def test_get_currencies(client):
    response = client.get('/currencies')
    assert response.status_code == 200
    currencies = response.json
    assert len(currencies) == 169
    assert 'USD' in currencies

def test_convert(client):
    response = client.post('/convert', json={
        "amount": 1,
        "curr_source": "USD",
        "curr_result": "CAD"
    },)
    assert response.status_code == 200
    json = response.json
    assert json == {"source_currency": "USD",
            "result_currency": "CAD",
            "exchange_rate": 1.361598,
            "converted_amount": 1.361598}

def test_statistics(client):
    response = client.get('/stats/USD/CAD')
    assert response.status_code == 200
    stats = response.json
    assert stats is not None
    assert stats['current_rate'] == 1.361598
    assert stats['min_rate'] == 1.361598
    assert stats['max_rate'] == 1.362088
    assert stats['mean_rate'] == (1.361598 + 1.362088)/2

def test_chart(client):
    response = client.get('/chart/USD/CAD')
    assert response.status_code == 200
    assert response.json == {"chart_url": "http://www.testchart.com"}