import unittest, json
import azure.functions as func

from unittest import mock
from Heartbeat import main

class TestHeartbeat(unittest.TestCase):

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_heartbeat_create(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'ip': '192.168.1.1',
        'port': '1337',
        'status': 'ready',
        'region': 'eastus'
      }).encode('utf8')
    )

    expected_data = {
      'PartitionKey': 'eastus',
      'ip': '192.168.1.1',
      'port': '1337',
      'status': 'ready'
    }

    # Act
    result = main(request)
    
    server_id = json.loads(result.get_body()).get('server_id')
    expected_data['RowKey'] = server_id

    # Assert
    mock_table_service().create_table.assert_called_with(table_name, fail_on_exist=False)
    mock_table_service().insert_or_replace_entity.assert_called_with(table_name, expected_data)
    assert result.status_code == 200

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_heartbeat_update(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'
    server_id = 'test_id'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'ip': '192.168.1.1',
        'port': '1337',
        'status': 'ready',
        'region': 'eastus',
        'server_id': server_id
      }).encode('utf8')
    )

    expected_data = {
      'PartitionKey': 'eastus',
      'ip': '192.168.1.1',
      'port': '1337',
      'status': 'ready',
      'RowKey': server_id
    }

    # Act
    result = main(request)
    result_server_id = json.loads(result.get_body()).get('server_id')

    # Assert
    mock_table_service().create_table.assert_called_with(table_name, fail_on_exist=False)
    mock_table_service().insert_or_replace_entity.assert_called_with(table_name, expected_data)
    assert result_server_id == server_id
    assert result.status_code == 200

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_missing_ip(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'
    server_id = 'test_id'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'port': '1337',
        'status': 'ready',
        'region': 'eastus'
      }).encode('utf8')
    )

    # Act
    result = main(request)
    message = json.loads(result.get_body()).get('messages')[0]

    # Assert
    mock_table_service().create_table.assert_not_called()
    mock_table_service().insert_or_replace_entity.assert_not_called()
    assert result.status_code == 400
    assert 'ip' in message

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_missing_port(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'
    server_id = 'test_id'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'ip': '192.168.1.1',
        'status': 'ready',
        'region': 'eastus'
      }).encode('utf8')
    )

    # Act
    result = main(request)
    message = json.loads(result.get_body()).get('messages')[0]

    # Assert
    mock_table_service().create_table.assert_not_called()
    mock_table_service().insert_or_replace_entity.assert_not_called()
    assert result.status_code == 400
    assert 'port' in message

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_missing_status(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'
    server_id = 'test_id'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'ip': '192.168.1.1',
        'port': '1337',
        'region': 'eastus'
      }).encode('utf8')
    )

    # Act
    result = main(request)
    message = json.loads(result.get_body()).get('messages')[0]

    # Assert
    mock_table_service().create_table.assert_not_called()
    mock_table_service().insert_or_replace_entity.assert_not_called()
    assert result.status_code == 400
    assert 'status' in message

  @mock.patch('Heartbeat.os')
  @mock.patch('Heartbeat.TableService')
  def test_missing_region(self, mock_table_service, mock_os):
    # Arrange
    table_name = 'servers'
    server_id = 'test_id'

    request = func.HttpRequest(
      method='POST',
      url='/api/heartbeat',
      body=json.dumps({
        'ip': '192.168.1.1',
        'port': '1337',
        'status': 'ready'
      }).encode('utf8')
    )

    # Act
    result = main(request)
    message = json.loads(result.get_body()).get('messages')[0]

    # Assert
    mock_table_service().create_table.assert_not_called()
    mock_table_service().insert_or_replace_entity.assert_not_called()
    assert result.status_code == 400
    assert 'region' in message
