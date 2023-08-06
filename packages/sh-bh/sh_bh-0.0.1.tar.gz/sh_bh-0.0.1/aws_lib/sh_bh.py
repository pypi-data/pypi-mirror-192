# function1
def create_s3_bucket():
    import boto3
    import uuid
    import time

    s3 = boto3.resource('s3')
    bucket_name = f"my-bucket-name-{str(uuid.uuid4())}-{str(int(time.time()))}"

    try:
        bucket = s3.create_bucket(Bucket=bucket_name)
    except s3.meta.client.exceptions.BucketAlreadyExists:
        print(f"Bucket name '{bucket_name}' is already taken. Trying again...")
        bucket_name = f"my-bucket-name-{str(uuid.uuid4())}-{str(int(time.time()))}"
        bucket = s3.create_bucket(Bucket=bucket_name)

    print(f"Bucket '{bucket_name}' created successfully.")


# function2
def create_iam_user():
    import boto3

    # Create an IAM client
    iam = boto3.client('iam')

    # Set the name of the user and the names of the policies
    user_name = input("Enter a username for the new IAM user: ")
    policy1_arn = input("Enter the ARN of the first policy to attach: ")
    policy2_arn = input("Enter the ARN of the second policy to attach: ")

    # Create the IAM user
    iam.create_user(UserName=user_name)

    # Attach the policies to the user
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy1_arn)
    iam.attach_user_policy(UserName=user_name, PolicyArn=policy2_arn)

    print(f"IAM user '{user_name}' created with policies '{policy1_arn}' and '{policy2_arn}'.")


# function3
def create_ec2_instance():
    import boto3

    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Get user inputs
    instance_name = input('Enter instance name: ')
    image_id = input('Enter AMI ID: ')
    instance_type = input('Enter instance type: ')
    key_name = input('Enter key pair name: ')
    security_group_ids = input('Enter comma-separated security group IDs: ').split(',')

    # Launch the instance
    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )

    # Get the instance ID
    instance_id = response['Instances'][0]['InstanceId']

    print(f'EC2 instance {instance_id} with name {instance_name} created')


# function4
def delete_s3_bucket():
    import boto3

    s3 = boto3.resource('s3')

    # List all available buckets
    buckets = [bucket.name for bucket in s3.buckets.all()]
    print(f"Available buckets: {buckets}")

    # Prompt the user to select a bucket to delete
    bucket_name = input("Enter the name of the bucket you want to delete: ")

    # Confirm the user's choice
    confirm = input(f"Are you sure you want to delete the '{bucket_name}' bucket? (yes/no): ")

    if confirm.lower() == 'yes':
        # Delete all objects in the bucket
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            obj.delete()

        # Delete the bucket
        bucket.delete()

        print(f"Bucket '{bucket_name}' deleted successfully.")
    else:
        print("Bucket deletion cancelled.")


# function5
def delete_iam_user():
    import boto3

    # Create an IAM client
    iam = boto3.client('iam')

    # Set the name of the user to delete
    user_name = input("Enter the name of the IAM user to delete: ")

    # Delete the IAM user
    iam.delete_user(UserName=user_name)

    print(f"IAM user '{user_name}' deleted.")


# function6
def delete_ec2_instance():
    import boto3

    # Set up the EC2 client
    ec2 = boto3.client('ec2')

    # Prompt the user to enter the instance name
    instance_name = input("Enter the name of the instance to be deleted: ")

    # Use filters to get the instance ID of the instance to be deleted
    filters = [
        {'Name': 'tag:Name', 'Values': [instance_name]}
    ]
    response = ec2.describe_instances(Filters=filters)
    instances = response['Reservations'][0]['Instances']
    instance_id = instances[0]['InstanceId']

    # Terminate the instance
    ec2.terminate_instances(InstanceIds=[instance_id])

    # Add a tag to the instance to indicate it has been terminated
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': f'{instance_name}-terminated'}]
    )

    print(f"Instance {instance_name} ({instance_id}) has been terminated.")
