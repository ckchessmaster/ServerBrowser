import datetime
import logging

import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService

def main(mytimer: func.TimerRequest) -> None:
  logging.info('Running server cleanup...')

  table_name = 'servers'
  table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])

  servers = table_service.query_entities(table_name)
  servers_to_expire = []

  for server in servers:
    last_heartbeat = server.timestamp

  logging.info('Server clean complete!')