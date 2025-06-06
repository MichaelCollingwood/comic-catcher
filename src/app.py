import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function that logs 'Hello World'
    """
    logger.info("Hello World")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World')
    } 