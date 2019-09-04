import json
import unittest
import time
from api import factory
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
		self.dummy_image_data = {
			"imageData": 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgDTD2qgAAAAASUVORK5CYII=',
			}	
			
	def test_post_resize_image(self):
		response = self.client.post(path='/api/v1/resize', data=json.dumps(self.dummy_image_data), content_type='application/json')
		self.assertEqual(response.status_code, 202)
		self.assertEqual(response.json['success'], True)
		self.assertIsNotNone(response.json['token'])

	def test_get_status_in_progress(self):
		post_response = self.client.post(path='/api/v1/resize', data=json.dumps(self.dummy_image_data), content_type='application/json')
		task_id = post_response.json['token']
		response = self.client.get(path='/api/v1/status', data=json.dumps(dict(token=task_id)), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], "IN_PROGRESS")
		self.assertIsNone(response.json['resized_image_url'])		

	def test_get_status_success(self):
		post_response = self.client.post(path='/api/v1/resize', data=json.dumps(self.dummy_image_data), content_type='application/json')
		task_id = post_response.json['token']
		time.sleep(0.5)
		response = self.client.get(path='/api/v1/status', data=json.dumps(dict(token=task_id)), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], "SUCCESS")
		self.assertIsNotNone(response.json['resized_image_url'])


if __name__ == '__main__':
	unittest.main()
