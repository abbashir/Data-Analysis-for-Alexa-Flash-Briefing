import boto3

# Create a Boto3 session obejct with your IAM user credentials
session = boto3.Session(
    aws_access_key_id='AKIASJA5X3GGW7IMZMEM',
    aws_secret_access_key='osc2Anvvvvt9HS853w+/eSPBKzRmYxgRo0vT4ImH',
)

s3 = session.resource('s3', region_name='us-east-1')
object = s3.Object('flushbriefing', 'data.json')
object.put(Body=open('new.json', 'rb'), ACL='public-read')



print('Upload test from royel')