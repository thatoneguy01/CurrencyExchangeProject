import pytest
import os
from webapp.app import create_app as create_frontend_app
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture()
def app(mocker):
    app = create_frontend_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_home(client, requests_mock):
    requests_mock.get(os.getenv("ANALYSIS_BASE_URL")+"/currencies", json=["USD", "CAD"])
    requests_mock.get(os.getenv("ANALYSIS_BASE_URL")+"/stats/USD/CAD", json={
                                                                            'current_rate': 1.361598,
                                                                            'min_rate': 1.361598,
                                                                            'max_rate': 1.362088,
                                                                            'mean_rate': (1.361598 + 1.362088)/2
                                                                            })
    requests_mock.get(os.getenv("ANALYSIS_BASE_URL")+"/chart/USD/CAD", json={"chart_url": "https://play.teleporthq.io/static/svg/default-img.svg"})
    response = client.get("/")
    assert response.status_code == 200
    