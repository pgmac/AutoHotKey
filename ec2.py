#!/usr/bin/env python3

import os

def instance_tag(instance_obj, tag_name="Name"):
	for tag in instance_obj['Tags']:
		if tag['Key'] == tag_name:
			return(tag['Value'])
	else:
		#return("[noname]")
		return(instance_obj['PrivateIpAddress'])

def display_host(host_dets, sep="@", num_keys=3):
	print("{}{}{}{}{}".format(host_dets['user'], sep, host_dets['host'], sep, host_dets['desc']), end="")
	if num_keys > 3:
		print("{}{}".format(sep, host_dets['key-pair']), end="")
	print("\n")
	

def describe_aws():
	import boto3
	ec2 = boto3.client('ec2')
	response = ec2.describe_instances()

	"""
	for instance in response.Reservations.Instances:
		display_host(showit)
	"""
	for key, value in response.items():
		if key == "Reservations":
			for reservation in value:
				showit = {}
				for instance in reservation['Instances']:
					try:
						showit['user'] = os.environ['USER']
					except KeyError:
						showit['user'] = "pmacdonnell"
					try:
						#showit['host'] = instance['PublicIpAddress']
						showit['host'] = instance['PrivateIpAddress']
					except KeyError:
						showit['host'] = "borked"
					try:
						showit['desc'] = instance_tag(instance, 'Name')
					except KeyError:
						showit['desc'] = "[noname]"
					try:
						showit['key-pair'] = instance_tag(instance, 'key-name')
					except KeyError:
						showit['key-pair'] = "[nokey]"
					display_host(showit, "@", 4)
					#print("{}@{}@{}".format(os.environ['USER'], instance['PrivateIpAddress'], instance_tag(instance, "Name")))
				
def describe_static():
	hosts = [
		{'user': 'paul', 'host': '192.168.10.178', 'desc': 'paul-cs'},
		{'user': 'admin', 'host': '192.168.10.1', 'desc': 'FW-01'},
		{'user': 'admin', 'host': '192.168.10.2', 'desc': 'FW-02'},
		{'user': 'paul', 'host': '172.22.22.7', 'desc': 'micro'},
		{'user': 'paul', 'host': '172.22.22.245', 'desc': 'marvin'}
	]
	for host in hosts:
		display_host(host)


if __name__ == '__main__':
	describe_aws()
	describe_static()
