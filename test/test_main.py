# test_main.py

"""
This module is used in accest to -> from chapp.main import app
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/")))

# Libraries
import json
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app

# Mock files
mock_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [102.0, 0.5]
                },
                "properties": {
                    "name": "Mock Location"
                }
            }
        ]
    }

# Create mock strings
mock_string1 = "mock_string1"
mock_string2 = "mock_string2"

# Create a TestClient instance
client = TestClient(app)

# Create the mock response
mock_response = {"result": "success"}

# Test for Error status code
def test_error_status_code_get_mean_ndvi():
    "asserting status code"
    response = client.get("/mean_ndvi_wg")
    assert response.status_code == 404
    assert response.json() == {'detail': 'The data could not be converted to bbox'}

def test_error_status_code_get_mean_ndvi_with_post():
    "asserting status code"
    response = client.post("/mean_ndvi_wp")
    # Due to the need to upload file
    assert response.status_code == 422
    assert response.json() ==  {'detail': [{'loc': ['body', 'Geojson_file'], 'msg': 'field required', 'type': 'value_error.missing'}]} != {'detail': 'The data could not be converted to bbox'}

# Test for 200 status code
def test_status_code_get_mean_ndvi():
    # Make the GET request
    response = client.get("/mean_ndvi_wg", params={
        "geojson": json.dumps(mock_geojson),
        "string1": mock_string1,
        "string2": mock_string2
    })

    # Assert that the response is valid
    assert response.status_code == 404
    assert response.json() == {'detail': 'The data could not be converted to bbox'}

def test_status_code_get_mean_ndvi_with_post():
    # Make the POST request
    response = client.post("/mean_ndvi_wg", params={
        "geojson": json.dumps(mock_geojson),
        "string1": mock_string1,
        "string2": mock_string2
    })

    # Assert that the response is valid
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}

# Special case :)
def test_greetings():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Greetings to everyone at UP42!!!!"}