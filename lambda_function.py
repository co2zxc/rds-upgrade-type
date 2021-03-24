import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    dims = json.loads(event["Records"][0]["Sns"]["Message"])['Trigger']['Dimensions']
    for dim in dims:
        if dim['name'] == 'InstanceId':
            instance_id = dim['value']
    print(instance_id)
    
    client = boto3.client('ec2')
    
    # Stop
    client.stop_instances(InstanceIds=[instance_id])
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    # Change
    client.modify_instance_attribute(InstanceId=instance_id, 
    Attribute='instanceType', Value='t2.medium')

    # Start
    client.start_instances(InstanceIds=[instance_id])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }