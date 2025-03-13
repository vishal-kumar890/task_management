# autoscale.py
import boto3
import os
import time
import django
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
django.setup()

# Now we can import Django models
from tasks.models import Task

def get_task_metrics():
    # Count tasks created in the last hour
    tasks_last_hour = Task.objects.filter(
        created_at__gte=datetime.now() - timedelta(hours=1)
    ).count()
    
    logger.info(f"Current task volume: {tasks_last_hour} tasks in the last hour")
    
    return {
        'tasks_per_hour': tasks_last_hour
    }

def adjust_capacity(metrics):
    # Define thresholds for scaling
    LOW_THRESHOLD = int(os.environ.get('LOW_THRESHOLD', 50))    # tasks per hour
    HIGH_THRESHOLD = int(os.environ.get('HIGH_THRESHOLD', 200)) # tasks per hour
    
    # Initialize AWS clients
    autoscaling_client = boto3.client('autoscaling')
    
    asg_name = os.environ.get('AUTO_SCALING_GROUP_NAME')
    if not asg_name:
        logger.error("AUTO_SCALING_GROUP_NAME environment variable not set")
        return
    
    # Get current capacity
    try:
        response = autoscaling_client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
        
        if not response['AutoScalingGroups']:
            logger.error(f"Auto Scaling Group {asg_name} not found")
            return
            
        current_capacity = response['AutoScalingGroups'][0]['DesiredCapacity']
        min_capacity = response['AutoScalingGroups'][0]['MinSize']
        max_capacity = response['AutoScalingGroups'][0]['MaxSize']
        
        logger.info(f"Current capacity: {current_capacity} instances (min: {min_capacity}, max: {max_capacity})")
        
        # Determine if scaling is needed
        if metrics['tasks_per_hour'] > HIGH_THRESHOLD and current_capacity < max_capacity:
            # Scale up
            new_capacity = min(current_capacity + 1, max_capacity)
            autoscaling_client.set_desired_capacity(
                AutoScalingGroupName=asg_name,
                DesiredCapacity=new_capacity
            )
            logger.info(f"Scaling up from {current_capacity} to {new_capacity} instances")
            
        elif metrics['tasks_per_hour'] < LOW_THRESHOLD and current_capacity > min_capacity:
            # Scale down
            new_capacity = max(current_capacity - 1, min_capacity)
            autoscaling_client.set_desired_capacity(
                AutoScalingGroupName=asg_name,
                DesiredCapacity=new_capacity
            )
            logger.info(f"Scaling down from {current_capacity} to {new_capacity} instances")
        else:
            logger.info("No scaling action needed")
            
    except Exception as e:
        logger.error(f"Error adjusting capacity: {str(e)}")

def main():
    logger.info("Starting auto-scaling monitor")
    
    check_interval = int(os.environ.get('CHECK_INTERVAL', 300))  # 5 minutes by default
    
    while True:
        try:
            metrics = get_task_metrics()
            adjust_capacity(metrics)
        except Exception as e:
            logger.error(f"Error in auto-scaling loop: {str(e)}")
            
        logger.info(f"Sleeping for {check_interval} seconds")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()