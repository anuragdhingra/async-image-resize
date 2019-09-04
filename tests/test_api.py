from api import create_app
from api import factory
import json
import unittest
from mock import MagicMock 

class TestApi(unittest.TestCase):

	def setUp(self):
		factory.get_app_config= MagicMock()
		factory.get_app_config.return_value = ['redis://localhost:6379/0', 'redis://localhost:6379/0']
		self.app = create_app()
		self.client = self.app.test_client()
		self.dummyImageData = {
			"imageData": "some base64 encoded image",
			}
		self.dummyToken = {
			"token": "f1c2e157-7b4c-4855-9e74-be3c9d71df17.jpg"
		}	
			
	def test_post_resize_image(self):
		resp = self.client.post(path='/api/v1/resize', data=json.dumps(self.dummyImageData), content_type='application/json')
		self.assertEqual(resp.status_code, 202)
		self.assertEqual(resp.json['success'], True)
		self.assertIsNotNone(resp.json['token'])

	def test_get_status(self):
		resp = self.client.get(path='/api/v1/status', data=json.dumps(self.dummyToken), content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json['status'], "PENDING")
		self.assertIsNone(resp.json['resized_image_url'])

if __name__ == '__main__':
	unittest.main()