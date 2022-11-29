from __future__ import print_function
from function_variables import *

import json
import boto3

def lambda_handler(event, context):
	print("Received event: " + json.dumps(event))
	service_group = event['detail']['group']
	container_instance = event['detail']['containerInstanceArn']

	if event['detail']['clusterArn'] not in clusters:
		print("Cluster is not being monitored. No action taken.")
		return 0

	if service_group not in target_groups:
		print("Service is not in Target Groups. No action taken.")
		return 0

	if event['detail']['lastStatus'] == "RUNNING" and event['detail']['desiredStatus'] == "RUNNING" and event['detail']['connectivity'] == "CONNECTED":
		#add to TG if lastStatus and desiredStatus are RUNNING
		elbclient = boto3.client('elbv2')
		ecsclient = boto3.client('ecs')
		hostPort = event['detail']['containers'][0]['networkBindings'][0]['hostPort']

		instance_info = ecsclient.describe_container_instances(
		    cluster=event['detail']['clusterArn'],
		    containerInstances=[
		        container_instance
		    ]
		)

		#add to tg
		elb_register = elbclient.register_targets(
		    TargetGroupArn=target_groups[service_group],
		    Targets=[

		        {
					'Id': instance_info['containerInstances'][0]['ec2InstanceId'],
		            'Port': hostPort
		        }
		    ]
		)
		print(json.dumps(elb_register))
	elif event['detail']['lastStatus'] == "RUNNING" and event['detail']['desiredStatus'] == "STOPPED"  and event['detail']['connectivity'] == "CONNECTED":
		#remove from tg if lastStatus is RUNNING and desiredStatus is STOPPED
		elbclient = boto3.client('elbv2')
		ecsclient = boto3.client('ecs')
		hostPort = event['detail']['containers'][0]['networkBindings'][0]['hostPort']
		instance_info = ecsclient.describe_container_instances(
		    cluster=event['detail']['clusterArn'],
		    containerInstances=[
		        container_instance
		    ]
		)

		#remove from tg
		elb_deregister = elbclient.deregister_targets(
		    TargetGroupArn=target_groups[service_group],
		    Targets=[
		        {
		            'Id': instance_info['containerInstances'][0]['ec2InstanceId'],
		            'Port': hostPort
		        },
		    ]
		)
		print(json.dumps(elb_deregister))
		return 0
	else:
		return 0