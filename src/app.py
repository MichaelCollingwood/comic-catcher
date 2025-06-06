import json
import logging
import os
import boto3

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
            'body': json.dumps('SMS sent successfully')
        }
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending SMS: {str(e)}')
        } 