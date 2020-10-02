import boto3

region = 'us-east-2'
instances = ['i-03bba575a1ced','i-060f9cd976c065','i-08854b63886bde','i-0bc80643a2b2bb','i-0dd7355fe1c96d']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
        for id in instances:
            ec2.instances.stop(id)
            print("Stopping Instance = {} of region = {} ".format(id, reg))
