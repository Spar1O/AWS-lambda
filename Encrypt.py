import json
import boto3

def lambda_handler(event, context):
    response = client.describe_volumes()
    volume=response['Volumes']
    y=0
    # for volume in response:
    volumeid = volume[y]['VolumeId']
    avlZone = volume[y]['AvailabilityZone']
    encrypted = volume[y]['Encrypted']
    volumeType = volume[y]['VolumeType']
    instanceId = volume[y]['Attachments'][y]['InstanceId']
    volSize= volume[y]['Size']
    devicename= volume[y]['Attachments'][y]['Device']

    y+=1
    if not encrypted:

        response2 = client.create_snapshot(
            Description='EBS_Snapshot' + volumeid,
            VolumeId=volumeid
        )

        time.sleep(30)

        response3 = client.create_volume(
            AvailabilityZone=avlZone,
            Encrypted=True,
            Size=volSize,
            SnapshotId=response2['SnapshotId'],
            VolumeType='gp2'
        )
        client.stop_instances(
            InstanceIds=[instanceId]
        )
        time.sleep(30)
        # detach ebs volume only after stopping instance
        client.detach_volume(
            Device=devicename,
            Force=True,
            InstanceId=instanceId,
            VolumeId=volumeid,
        )
        time.sleep(20)
        client.attach_volume(
            Device='/dev/xvda',
            InstanceId = instanceId,
            VolumeId= response3['VolumeId'],

        )
        time.sleep(30)
        client.start_instances(
            InstanceIds=[instanceId]
        )
