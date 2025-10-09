import boto3
import json

sts_client = boto3.client('sts')
account_id = sts_client.get_caller_identity()['Account']
role = sts_client.get_caller_identity()['Arn'].split(':')[5]
print("Credentials from the local environment:")
print("Account ID: %s" % account_id)
print("Identity: %s" % role)
if account_id == '730335390515':
    secret_name = "dev/silicon_mark_backend"
else:
  secret_name = "prod/silicon_mark_backend"

region_name = "us-east-1"
user_pool_id = "us-east-1_yovKUEwdp"
cognito_role_arn = "arn:aws:iam::730335390515:role/CognitoAccessRole"

# Assume a role in the Sandbox account to access Cognito
assumed_role_object=sts_client.assume_role(
    RoleArn=cognito_role_arn,
    RoleSessionName="CognitoSession"
)
credentials=assumed_role_object['Credentials']

Session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
cognito_client = Session.client('cognito-idp', region_name='us-east-1')
response = cognito_client.list_users(
    UserPoolId=user_pool_id,
    Limit=5
)
print("User Pool ID: %s" % user_pool_id)
print ("Sampled Cognito Users:")
for user in response['Users']:
    print("Username: %s" % user['Username'])
    print("Attributes:")
    for attr in user['Attributes']:
        print("  %s: %s" % (attr['Name'], attr['Value']))
    print("\n")


# Set the old access key AWS credentials from the secret
# Create a Secrets Manager client to get the access key
sm_client = boto3.client(
    service_name='secretsmanager',
    region_name=region_name
)
get_secret_value_response = sm_client.get_secret_value(
      SecretId=secret_name
)
secret_dict = json.loads(get_secret_value_response['SecretString'])
# Extract AWS credentials from the AWS_CONFIG object
aws_config = secret_dict['AWS_CONFIG']
aws_access_key_id = aws_config['aws_access_key_id']
aws_secret_access_key = aws_config['aws_secret_access_key']
sts_client_ak = boto3.client('sts',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
account_id = sts_client_ak.get_caller_identity()['Account']
role = sts_client_ak.get_caller_identity()['Arn'].split(':')[5]
print("Credentials using the access key:")
print("Account ID: %s" % account_id)
print("Identity: %s" % role)
