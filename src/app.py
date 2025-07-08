import json
import logging
import os
import boto3

from src.utils import load_yaml
from src.web_crawling import extract_relevant_events_from_bill_murray_homepage

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    Lambda function that sends 'Hello World' via SMS
    """
    try:
        # Logic for web scraping here. Output is an array of urls for websites to check
        comedians = load_yaml('comedians.yaml')['comedians']
        comedians_and_urls = extract_relevant_events_from_bill_murray_homepage(comedians)
        if len(comedians_and_urls) > 0:
            # Get the SNS topic ARN from environment variables
            topic_arn = os.environ['SNS_TOPIC_ARN']

            # Publish message to SNS topic
            response = sns.publish(
                TopicArn=topic_arn,
                Message='Hello World',
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'HelloApp'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )

            logger.info(f"Message sent successfully: {response['MessageId']}")
            return {
                'statusCode': 200,
                'body': json.dumps('SMS sent successfully.')
            }

        else:
            return {
                'statusCode': 200,
                'body': json.dumps('No SMS sent.')
            }

    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending SMS: {str(e)}')
        } 