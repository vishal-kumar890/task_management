import os,json,logging
from datetime import datetime

logger = logging.getLogger(__name__)

def send_task_completed_notification(task):
    # we'll just log the notification to simulatesend notification to lambda function
    
    task_data = {
        'task_id':task.id,
        'Taskname':task.task_name,
        'CompletedAt':datetime.now().isoformat(),
        'AssignedTo':task.assigned_to.username,
        'AssignedToEmail':task.assigned_to.email,
    }

    # SIMULATE AWS LAMBDA INVOCATION
    lambda_function_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'task-notification')
    region = os.environ.get('AWS_REGION', 'us-east-1')

    logger.info(f"Simulating AWS Lambda invocation: {lambda_function_name} in {region}")
    logger.info(f"Payload: {json.dumps(task_data)}")

    # We would use boto3 like this to call lambda function:
    # import boto3
    # lambda_client = boto3.client('lambda', region_name=region)
    # response = lambda_client.invoke(
    #     FunctionName=lambda_function_name,
    #     InvocationType='Event',  # Asynchronous
    #     Payload=json.dumps(task_data)
    # )

    return True