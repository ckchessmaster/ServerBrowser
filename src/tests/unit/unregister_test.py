import unittest, json
import azure.functions as func

from unittest import mock
from Unregister import main

class TestUnregister(unittest.TestCase):

  @mock.patch('Unregister.os')
  @mock.patch('Unregister.TableService')
  def test_unregister(self, mock_table_service, mock_os):
    # Arrange
    server_id = 'some-id'
    region = 'eastus'

    request = func.HttpRequest(
      method='DELETE',
      url='/api/unregister',
      body=None,
      params={ 'server-id': server_id, 'region': region }
    )

    # Act
    result = main(request)
    response_message = json.loads(result.get_body()).get('message')

    # Assert
    assert result.status_code == 200
    assert f'{server_id} successfully' in response_message 
    mock_table_service().delete_entity.assert_called_with('servers', region, server_id)

  @mock.patch('Unregister.os')
  @mock.patch('Unregister.TableService')
  def test_missing_server_id(self, mock_table_service, mock_os):
    # Arrange
    region = 'eastus'

    request = func.HttpRequest(
      method='DELETE',
      url='/api/unregister',
      body=None,
      params={ 'region': region }
    )

    # Act
    result = main(request)
    response_message = json.loads(result.get_body()).get('message')

    # Assert
    assert result.status_code == 400
    assert 'server-id' in response_message 
    mock_table_service().delete_entity.assert_not_called()

  @mock.patch('Unregister.os')
  @mock.patch('Unregister.TableService')
  def test_missing_server_id(self, mock_table_service, mock_os):
    # Arrange
    server_id = 'some-id'

    request = func.HttpRequest(
      method='DELETE',
      url='/api/unregister',
      body=None,
      params={ 'server-id': server_id }
    )

    # Act
    result = main(request)
    response_message = json.loads(result.get_body()).get('message')

    # Assert
    assert result.status_code == 400
    assert 'region' in response_message 
    mock_table_service().delete_entity.assert_not_called()

  @mock.patch('Unregister.os')
  @mock.patch('Unregister.TableService')
  def test_server_not_found(self, mock_table_service, mock_os):
    # Arrange
    server_id = 'some-id'
    region = 'region'

    request = func.HttpRequest(
      method='DELETE',
      url='/api/unregister',
      body=None,
      params={ 'server-id': server_id, 'region': region }
    )

    mock_table_service().delete_entity.side_effect = ValueError()

    # Act
    result = main(request)
    response_message = json.loads(result.get_body()).get('message')

    # Assert
    assert result.status_code == 400
    assert f'{server_id} not found' in response_message 
    mock_table_service().delete_entity.assert_called_with('servers', region, server_id)
