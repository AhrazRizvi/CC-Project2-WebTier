import boto3

# Set up a connection to the EC2 resource in the desired AWS region
ec2_resource = boto3.resource('ec2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Configuration parameters for the instance
ami_image_id = "ami-0a0e5d9c7acc336f1"
key_pair_name = "cse546temp"
security_group_list = ["sg-08fe2e218cf628649"]

# Read the startup script (user data) from a text file
with open("cc-startup-script.txt", "r") as script_file:
    startup_script = script_file.read()

# Launch a new EC2 instance with the specified settings
new_instance = ec2_resource.create_instances(
    ImageId=ami_image_id,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=key_pair_name,
    SecurityGroupIds=security_group_list,
    UserData=startup_script,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'my-web-instance'}]
    }]
)

# Ensure the instance is up and running before proceeding
new_instance[0].wait_until_running()

# Get the instance ID
instance_id = new_instance[0].id
print(f"Successfully launched instance with ID: {instance_id}")

# Allocate an Elastic IP (EIP)
allocation = ec2_client.allocate_address(Domain='vpc')

# Associate the allocated Elastic IP with the instance
response = ec2_client.associate_address(
    InstanceId=instance_id,
    AllocationId=allocation['AllocationId']
)

# Output the Elastic IP assigned
print(f"Elastic IP {allocation['PublicIp']} assigned to instance {instance_id}")
