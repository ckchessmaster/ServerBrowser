import json

import azure.functions as func

def create_function_response(body, status_code):
  return func.HttpResponse(
    body=json.dumps(body), 
    status_code=status_code,
    mimetype='application/json',
    charset='utf-8')
