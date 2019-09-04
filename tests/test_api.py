from api import factory
import json
import unittest
from mock import MagicMock 


def _get_mock_celery_config():
	return {
		'CELERY_BROKER_URL': 'redis://localhost:6379/0',
		'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0'
	}


class TestApi(unittest.TestCase):

	def setUp(self):
		factory.get_celery_config = MagicMock()
		factory.get_celery_config.return_value = _get_mock_celery_config()
		self.app = factory.create_app()
		self.client = self.app.test_client()
		self.dummyImageData = {
			"imageData": "some base64 encoded image",
			}
		self.dummyToken = {
			"token": "f1c2e157-7b4c-4855-9e74-be3c9d71df17.jpg"
		}	
			
	def test_post_resize_image(self):
		response = self.client.post(path='/api/v1/resize', data=json.dumps(self.dummyImageData), content_type='application/json')
		self.assertEqual(response.status_code, 202)
		self.assertEqual(response.json['success'], True)
		self.assertIsNotNone(response.json['token'])

	def test_get_status(self):
		response = self.client.get(path='/api/v1/status', data=json.dumps(self.dummyToken), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], "PENDING")
		self.assertIsNone(response.json['resized_image_url'])


if __name__ == '__main__':
	unittest.main()
