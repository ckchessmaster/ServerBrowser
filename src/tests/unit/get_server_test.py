import unittest, json
import azure.functions as func

from unittest import mock
from GetServer import main

class FakeServer:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port

class TestGetServer(unittest.TestCase):

  @mock.patch('GetServer.os')
  @mock.patch('GetServer.TableService')
  def test_get_server(self, mock_table_service, mock_os):
    # Arrange
    request = func.HttpRequest(
      method='GET',
      url='/api/getserver',
      params={ 'region': 'eastus' },
      body=None
    )

    ip = '123.456.789.100'
    port = '1234'

    expected_data = {
      'server': {
        'ip': ip,
        'port': port
      }
    }

    mock_table_service().query_entities.return_value = [FakeServer(ip, port), FakeServer('anotherIP', 'anotherPort')]

    # Act
    response = main(request)

    # Assert
    assert response.status_code == 200
    assert json.loads(response.get_body()) == expected_data

  @mock.patch('GetServer.os')
  @mock.patch('GetServer.TableService')
  def test_no_server(self, mock_table_service, mock_os):
    # Arrange
    request = func.HttpRequest(
      method='GET',
      url='/api/getserver',
      params={ 'region': 'eastus' },
      body=None
    )

    mock_table_service().query_entities.return_value = []

    # Act
    response = main(request)

    # Assert
    assert response.status_code == 200
    assert 'No servers are currently available' in json.loads(response.get_body()).get('message')

  @mock.patch('GetServer.os')
  @mock.patch('GetServer.TableService')
  def test_missing_region(self, mock_table_service, mock_os):
    # Arrange
    request = func.HttpRequest(
      method='GET',
      url='/api/getserver',
      body=None
    )

    # Act
    response = main(request)

    # Assert
    assert response.status_code == 400
    assert 'region' in json.loads(response.get_body()).get('message')
    