import logging, json
import azure.functions as func

from Util import http_utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a health request.')

    func.HttpResponse.mimetype = 'application/json'
    func.HttpResponse.charset = 'utf-8'

    response = {
      'healthy': True
    }

    return http_utils.create_function_response(response, 200)
