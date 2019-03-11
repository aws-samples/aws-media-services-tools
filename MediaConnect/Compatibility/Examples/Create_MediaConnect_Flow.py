import boto3

Avilability_Zone = 'us-west-2a'
Flow_Name = 'test_flow'
Input_Source = {
    ## TODO: find a better way to handle this
    'Decryption': {
        'Algorithm': 'aes128',
        'KeyType': 'static-key', # default
        'RoleArn': 'arn'
    }
}

Output_Destinations = [
    {
    ## TODO: find a way to handle this elegantly
    }
]


client = boto3.client('mediaconnect')

# create a flow
flow = client.create_flow(
    AvailabilityZone = Availability_Zone,
    Name=Flow_Name,
    Source=Input_Source)



# create an output
output = client.add_flow_outputs(
    FlowArn=flow['Flow']['FlowArn'],
    Outputs = Output_Destinations
)
