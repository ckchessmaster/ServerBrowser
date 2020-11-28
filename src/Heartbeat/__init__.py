import logging, json, uuid, os
import azure.functions as func

from Util import http_utils
from azure.cosmosdb.table.tableservice import TableService

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  try:
    body = req.get_json()
    validation_messages = validate(body)

    if len(validation_messages) > 0:
      return http_utils.create_function_response({ 'messages': validation_messages }, 400)

    row_key = body.get('server_id') if body.get('server_id') else str(uuid.uuid4())

    data = {
      'RowKey': row_key,
      'PartitionKey': body.get('region'),
      'ip': body.get('ip'),
      'port': body.get('port'),
      'status': body.get('status')
    }

    table_name = 'servers'
    table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
    table_service.create_table(table_name, fail_on_exist=False)
    table_service.insert_or_replace_entity(table_name, data)

    return http_utils.create_function_response({ 'messages': 'Server heartbeat successful.', 'server_id': row_key }, 200)

  except ValueError:
    return http_utils.create_function_response({ 'message': 'Missing required payload' }, 400)

def validate(body):
  messages = []

  base_message = 'Missing required parameter: '

  if not body.get('ip'):
    messages.append(base_message + 'ip')

  if not body.get('port'):
    messages.append(base_message + 'port')

  if not body.get('status'):
    messages.append(base_message + 'status')

  if not body.get('region'):
    messages.append(base_message + 'region')

  return messages