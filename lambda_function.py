import json
import boto3
import random
import string


def lambda_handler(event, context):
    client = boto3.client('rds')

    cluster_id = 'poc-postgresql'
    new_id = ''.join(random.choices(string.ascii_uppercase, k=10))
    
    new_id_vv = cluster_id+"-"+new_id
    
    response = client.describe_db_clusters(
        DBClusterIdentifier=cluster_id,
    )
    
    members = response['DBClusters'][0]['DBClusterMembers']
    
    for member in members:
        if member['IsClusterWriter']:
            writer_id = member['DBInstanceIdentifier']
    
    response = client.create_db_instance(
        #DBInstanceIdentifier=new_id,
        DBInstanceIdentifier=new_id_vv,
        DBInstanceClass='db.r5.2xlarge',
        Engine='aurora-postgresql',
        DBClusterIdentifier=cluster_id)
    
    waiter = client.get_waiter('db_instance_available')
    
    #waiter.wait(DBInstanceIdentifier=new_id)
    waiter.wait(DBInstanceIdentifier=new_id_vv)
        
    response = client.failover_db_cluster(
        DBClusterIdentifier=cluster_id,
        #TargetDBInstanceIdentifier=new_id
        TargetDBInstanceIdentifier=new_id_vv
    )
    
    
    
    response = client.delete_db_instance(
        DBInstanceIdentifier=writer_id
    )


