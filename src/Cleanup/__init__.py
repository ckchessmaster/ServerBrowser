import datetime, logging, os

import azure.functions as func
from datetime import datetime, timezone
from azure.cosmosdb.table.tableservice import TableService, TableBatch

def main(mytimer: func.TimerRequest) -> None:
  logging.info('Running server cleanup...')

  table_name = 'servers'
  table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
  batch = TableBatch()

  servers = table_service.query_entities(table_name)

  for server in servers:
    last_heartbeat = server.lastHeartbeatTime
    current_time = datetime.now(timezone.utc)
    seconds_since_last_heartbeat = current_time - last_heartbeat

    if seconds_since_last_heartbeat.total_seconds() >= int(os.environ['HeartbeatTimeoutSeconds']):
      batch.delete_entity(server.partition_key, server.row_key)

  table_service.commit_batch(table_name, batch)

  logging.info('Server clean complete!')