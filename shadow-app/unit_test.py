import unittest
from unittest import mock
import shadow_api


valid_username = 'pyreporter'
invalid_username = 'pyrepor*(&08yg880)Yter123'
shadowban_username = 'FlashyInsurance1337'
class TestShadowAPI(unittest.TestCase):
    def setUp(self):
        self.app = shadow_api.app.test_client()

    def test_valid_username(self):
        response = self.app.get(f'/shadowban/{valid_username}')
        self.assertEqual(response.status_code, 200)

    def test_invalid_username(self):
        response = self.app.get(f'/shadowban/{invalid_username}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'Invalid username'})

    def test_username_shadowbanned(self):
        response = self.app.get(f'/shadowban/{shadowban_username}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'is_shadowbanned': True})

    def test_get_full_data(self):
        response = self.app.get(f'/shadowban/{valid_username}?full=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_shadowbanned', response.get_json())
        self.assertIn('username', response.get_json())
        self.assertIn('join_date', response.get_json())
        self.assertIn('post_karma', response.get_json())
        self.assertIn('comment_karma', response.get_json())
        self.assertIn('verified_mail', response.get_json())

    def test_post_method_not_allowed(self):
        response = self.app.post(f'/shadowban/{valid_username}')
        self.assertEqual(response.status_code, 405)

    def test_with_valid_client_credentials(self):
        response = self.app.get(f'/shadowban/{valid_username}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'is_shadowbanned': False})

    def test_internal_server_error(self):
        with mock.patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Internal Server Error")
            response = self.app.get(f'/shadowban/{valid_username}')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_data(as_text=True), '{"error":"Internal Server Error"}\n')

if __name__ == '__main__':
    unittest.main()
