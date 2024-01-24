import boto3, time

#api client
iam = boto3.client('iam')

#variables setttings
iam_username = '<YOUR-USER>'

try:
    #replace with a specific test user
    response = iam.create_access_key(UserName=iam_username)
    access_key = response['AccessKey']['AccessKeyId']
    secret_key = response['AccessKey']['SecretAccessKey']

    print("Access Key:", access_key)
    #print("Secret Key:", secret_key)
    time.sleep(3) #give API time to catch up

    #restore original state
    response = iam.delete_access_key(
        UserName=iam_username,
        AccessKeyId=access_key #required
    )
    print('IAM key generated and deleted successfully.')
except ValueError:
    print('IAM key was not successfully created and deleted for: ', iam_username)
    exit(1)

