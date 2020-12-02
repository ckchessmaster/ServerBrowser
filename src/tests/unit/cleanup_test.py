import unittest, json
import azure.functions as func

from unittest import mock
from Cleanup import main
from datetime import datetime, timezone
from .fakes.fake_server import FakeServer

class TestCleanup(unittest.TestCase):

  @mock.patch('Cleanup.TableBatch')
  @mock.patch('Cleanup.os')
  @mock.patch('Cleanup.TableService')
  def test_cleanup(self, mock_table_service, mock_os, mock_table_batch):
    # Arrange
    ip = '123.456.789.100'
    port = '1234'
    last_heartbeat_time = datetime(2020, 12, 1, 10, 0, 0, 0, timezone.utc)

    mock_table_service().query_entities.return_value = [FakeServer(ip, port, lastHeartbeatTime=last_heartbeat_time)]

    # Act
    main(None)

    # Assert
    mock_table_batch().delete_entity.assert_called()
    mock_table_service().commit_batch.assert_called()

  @mock.patch('Cleanup.TableBatch')
  @mock.patch('Cleanup.os')
  @mock.patch('Cleanup.TableService')
  def test_cleanup(self, mock_table_service, mock_os, mock_table_batch):
    # Arrange
    ip = '123.456.789.100'
    port = '1234'
    last_heartbeat_time = datetime.now(timezone.utc)

    mock_table_service().query_entities.return_value = [FakeServer(ip, port, lastHeartbeatTime=last_heartbeat_time)]

    # Act
    main(None)

    # Assert
    mock_table_batch().delete_entity.assert_not_called()
    mock_table_service().commit_batch.assert_called()