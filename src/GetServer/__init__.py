import logging, os
import azure.functions as func

from Util import http_utils
from azure.cosmosdb.table.tableservice import TableService

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Get server request recieved.')

  region = req.params.get('region')
  if not region:
    try:
      req_body = req.get_json()
    except ValueError:
      pass
    else:
      region = req_body.get('region')

  if not region:
    return http_utils.create_function_response({ 'message': 'Missing required parameter: region'}, 400)

  table_name = 'servers'
  table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])

  servers = list(table_service.query_entities(table_name, filter=f"PartitionKey eq '{region}'"))

  if len(servers) == 0:
    return http_utils.create_function_response({ 'message': 'No servers are currently available. Please try again in a few minutes.'}, 200)

  server = get_best_server(servers)

  return http_utils.create_function_response({
    'server': {
      'ip': server.ip,
      'port': server.port
    }
  },
  200)
    
def get_best_server(servers):
  return servers[0]