from app import app
from aws_lambda_wsgi import response

def lambda_handler(event, context):
    return response(app, event, context)