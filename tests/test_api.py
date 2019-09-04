from api import create_app
import json
import unittest

class TestApi(unittest.TestCase):

	def setUp(self):
		self.app = create_app(test_mode=True)
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