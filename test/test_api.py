import pytest
import json
from api.controller import routes
from api import create_app
from mock import MagicMock
import flask

app = create_app()

def test_resize_api(mocker):
        request_mock = mocker.patch.object(flask, "request")
        request_mock.json['imageData'].return_value = "abcd"
        # uuid.uuid4() = MagicMock(return_value="1234")
        result_json = routes.resize_image()
        print(result_json)
        # assert result_json.status_code == 202
        # assert result_json.success == True
        # assert result_json.token == "1234"

        # headers = {
        #     'Content-Type': json,
        # }
        # data = {
        #     'imageString': 'base64encodedstring'
        # }
        # url  = '/api/v1/resize/'
        # response = client.post(url,data=json.dumps(data),headers=headers)
        # assert response.status_code == 202
        # assert response.content_type == 'application/json'
        # assert response.json == {'success': 'true'}