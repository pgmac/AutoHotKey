#!/usr/bin/env python3

''' Will display a list of AWS EC2 instances suitable for use in my AutoHotKey servers script '''
import os


def instance_tag(instance_obj, tag_name="Name"):
    ''' Get a tag from the specified instance '''
    for tag in instance_obj['Tags']:
        if tag['Key'] == tag_name:
            return tag['Value']
    else:
        #return("[noname]")
        return instance_obj['PrivateIpAddress']


def display_host(host_dets, sep="@", num_keys=3):
    ''' Display the host entry to stdout '''
    print("{}{}{}{}{}".format(host_dets['user'], sep, host_dets['host'], sep, host_dets['desc']), end="")
    if num_keys > 3:
        print("{}{}".format(sep, host_dets['key-pair']), end="")
    print("\n", end="")


def describe_aws():
    ''' Get list of AWS EC2 instances '''
    import boto3

    _hosts = []
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
                    _hosts.append(showit)
                    #display_host(showit, "@", 4)
                    #print("{}@{}@{}".format(os.environ['USER'], instance['PrivateIpAddress'], instance_tag(instance, "Name")))
    return _hosts


def describe_static():
    ''' Build a list of static server entries '''
    _hosts = [
        {'user': 'pmacdonnell', 'host': 'ansible', 'desc': 'ansible control server'},
        {'user': 'paul', 'host': '192.168.10.178', 'desc': 'paul-cs'},
        {'user': 'admin', 'host': '192.168.10.1', 'desc': 'FW-01'},
        {'user': 'admin', 'host': '192.168.10.2', 'desc': 'FW-02'},
        {'user': 'csadmin', 'host': '192.168.10.6', 'desc': 'BNE-OPENVPN'},
        {'user': 'pi', 'host': '192.168.10.211', 'desc': 'RPI-01'},
        {'user': 'pi', 'host': '192.168.10.212', 'desc': 'RPI-02'},
        {'user': 'pi', 'host': '192.168.10.213', 'desc': 'RPI-03'},
        {'user': 'pi', 'host': '192.168.10.214', 'desc': 'RPI-04'},
        {'user': 'pi', 'host': '192.168.10.215', 'desc': 'RPI-05'},
        {'user': 'pi', 'host': '192.168.10.216', 'desc': 'RPI-06'},
        {'user': 'pi', 'host': '192.168.10.217', 'desc': 'RPI-07'},
        {'user': 'pi', 'host': '192.168.10.218', 'desc': 'RPI-08'},
        {'user': 'pi', 'host': '192.168.10.219', 'desc': 'RPI-09'},
        {'user': 'pi', 'host': '192.168.10.220', 'desc': 'RPI-10'},
        {'user': 'paul', 'host': '172.22.22.7', 'desc': 'micro'},
        {'user': 'paul', 'host': '172.22.22.245', 'desc': 'marvin'}
    ]
    return _hosts


if __name__ == '__main__':
    hosts = describe_aws()
    for host in describe_static():
        hosts.append(host)

    for host in hosts:
        display_host(host)