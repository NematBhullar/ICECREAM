"""
system test for the health checkpoint
"""
from http.client import OK
import requests
from ..config import BASE_ROUTE

def test_health_checkpoint():
    response = requests.get(BASE_ROUTE + "health")
    assert response.status_code == OK
    output = response.json()
    assert output['liveness'] == "up"
