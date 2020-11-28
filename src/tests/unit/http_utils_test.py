import unittest, json

from Util import http_utils

class TestHttpUtils(unittest.TestCase):
  def test_create_function_response(self):
    # Arrange
    body = { 'message': 'test' }
    status_code = 200

    # Act
    result = http_utils.create_function_response(body, status_code)

    # Assert
    assert json.loads(result.get_body()) == body
    assert result.status_code == status_code
    assert result.mimetype == 'application/json'
    assert result.charset == 'utf-8'
