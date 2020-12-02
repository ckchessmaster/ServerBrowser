import logging, os
import azure.functions as func

from Util import http_utils
from azure.cosmosdb.table.tableservice import TableService

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Unregister request recieved.')

    server_id = req.params.get('server-id')
    region = req.params.get('region')

    if not server_id:
      return http_utils.create_function_response({ 'message': 'Missing required parameter: server-id'}, status_code=400)

    if not region:
      return http_utils.create_function_response({ 'message': 'Missing required parameter: region' }, status_code=400)

    try:
      table_name = 'servers'
      table_service = TableService(connection_string=os.environ['AzureWebJobsStorage'])
      table_service.delete_entity(table_name, region, server_id)

      return http_utils.create_function_response({ 'message': f'Server {server_id} successfully unregistered.'}, 200)
    except:
      return http_utils.create_function_response({ 'message': f'Server {server_id} not found.'}, 400)