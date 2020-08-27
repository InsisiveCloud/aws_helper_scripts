#!/usr/bin/env python
import time
import boto3
from botocore.exceptions import ClientError
import json
import traceback
import argparse

def all_regions(client):
    for i in client.describe_regions()['Regions']:
        yield i['RegionName']


def fetch_instances(client, filters):
    next_token = ''
    all_instances = []
    base_filters = [
        {'Name': 'instance-state-name', 'Values': ['running']},
    ]
    if filters:
        base_filters.extend(filters)

    while True:
        resp = client.describe_instances(
            Filters=base_filters,
            NextToken=next_token
        )
        next_token = ''
        if 'NextToken' in resp and resp['NextToken']:
            next_token = resp['NextToken']
        reservations = resp['Reservations']
        for instances in reservations:
            for ins in instances['Instances']:
                instance = {
                    'instance_id': ins['InstanceId'],
                    'image_id': ins['ImageId'],
                    'instance_type': ins['InstanceType'],
                    'os_type': get_os_type(client, ins)
                }
                all_instances.append(instance)

        if not next_token:
            break
    return all_instances


def get_os_type(client, instance):
    if 'ImageId' not in instance:
        return

    image_id = instance['ImageId']
    try:
        resp = client.describe_images(ImageIds=[image_id])
        if resp['Images']:
            image_description = resp['Images']
            if 'Platform' in image_description:
                return image_description['Platform']
            if 'Description' in image_description:
                return image_description['Description']

    except ClientError as err:
        print('ERROR: Not able to fetch image type')

    return


def install_cloudwatch_agent(ssm, instance):
    response = ssm.send_command(
        Targets=[{'Key': 'InstanceIds', 'Values': [instance['instance_id']]}],
        DocumentName='AWS-ConfigureAWSPackage',
        DocumentVersion='$LATEST',
        Parameters={
            "action": ['Install'],
            'version': ['LATEST'],
            'name': ['AmazonCloudWatchAgent']
        },
        TimeoutSeconds=600,
    )
    command_id = response['Command']['CommandId']
    time.sleep(2)
    output = ssm.get_command_invocation(
        CommandId=command_id, InstanceId=instance['instance_id']
    )
    print({
        'InstanceId': output['InstanceId'],
        'CommandId': output['CommandId'],
    })
    return


def parse_filters(args):
    if args.instance_ids:
        return args.instance_ids
    if args.filters:
        return args.filters


def main(args):
    filters = parse_filters(args)
    client = boto3.client('ec2')
    for region in all_regions(client):
        ec2_client = boto3.client('ec2', region_name=region)
        all_instances = fetch_instances(ec2_client, filters)
        for instance in all_instances:
            try:
                ssm = boto3.client('ssm', region_name=region)
                install_cloudwatch_agent(ssm, instance)
            except Exception as e:
                print(instance['instance_id'])
                traceback.print_exc()

    return


def instance_list(string):
    return [{
        'Name': 'instance-id',
        'Values': string.split(','),
    }]


def filter_list(string):
    filter_list = string.split(',')
    final_list = []
    for item in filter_list:
        _filter = json.loads(item)
        for i in _filter:
            final_list.append(
                {'Name': 'tag:'+i, 'Values': [_filter[i]]}
            )
    return final_list


if __name__ == '__main__':
    description = """\n\tThis script is use to install CloudWatchAgent on the EC2 instances,
    \twith the given filter tags or instance ids. \n
    \tEither filters or instance id list is required in order to execute script
    \t$ python install_cloudwatch.py {-h, --help} # for more details\n"""

    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument(
        '-f', '--filters', required=False, type=filter_list, action='store',
        help='Tags for filtering instances \n eg: \'{"<tagname>": "<value>"}, ...\''
    )
    parser.add_argument(
        '-i', '--instance-ids', required=False, type=instance_list, action='store',
        help='List of \',\' seperated instance-ids where you want to install CloudWatch Agent'
    )
    args = parser.parse_args()
    if not args.instance_ids and not args.filters:
        print(description)
        exit(1)

    main(args)
