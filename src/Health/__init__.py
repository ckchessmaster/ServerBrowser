import logging, json

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a health request.')

    func.HttpResponse.mimetype = 'application/json'
    func.HttpResponse.charset = 'utf-8'

    response = {
      'healthy': True
    }

    return func.HttpResponse(
      body=json.dumps(response),
      status_code=200,
      mimetype='application/json'
    )
