import boto3

'''
How to use:
Modify the event and profile variable definitions and execute the script
python3 ./Create_MediaPackage_Channel.py

What does it do:
This script will create a MediaPackage channel with HLS input and playback,
Additionally, it will create SSM records that MediaLive will use to securely
push content to MediaPackage.  These credentials are returned as a data
structure that is required for the MediaLive channel creation script

Dependencies:
This script assumes an AWS CLI profile is avilable on the system it runs on
For information about setting up local authentication:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

Inputs:
You must provide an event dictionary, with an 'ID' field
'''

profile_name = 'the AWS CLI profile to use while creating MediaPackage Resources'
event = {
    "ID": "test channel",
}


# creates a MediaPackage channel
def create_mediapackage(client, Id):
    response = client.create_channel(
        Description="Channel: %s" % Id,
        Id=Id)
    ingest_points = response['HlsIngest']['IngestEndpoints']
    return ingest_points


# creates an MediaPackage endpoint for the MediaPackage channel
def create_package_endpoint(client, Id):
    response = client.create_origin_endpoint(
        ChannelId=Id,
        HlsPackage={
            'AdMarkers': "NONE",
            'IncludeIframeOnlyStream': False,
            'PlaylistType': 'EVENT',
            'PlaylistWindowSeconds': 60,
            'ProgramDateTimeIntervalSeconds': 0,
            'SegmentDurationSeconds': 6,
            'StreamSelection': {
                'MaxVideoBitsPerSecond': 2147483647,
                'MinVideoBitsPerSecond': 0,
                'StreamOrder': "ORIGINAL"
            }
        },
        Id=Id
    )
    return response['Url']

# checks to see if there is already a parameter store entry for
def param_store_entry_exists(client, ps_name):
    try:
        response = client.get_parameters(
            Names=[
                ps_name,
            ],
            WithDecryption=False
        )
        if len(response['Parameters']) == 0:
            return False
        else:
            return True
    except e:
        print("Exception raised:", repr(e.message))

# creates a parameter store entry if one doesn't already exist,
def create_param_store_entry(client, ps_name, ps_value, ps_description='later'):
    try:
        if not param_store_entry_exists(client, "/medialive/%s" % (ps_name)):
            reponse = client.put_parameter(Name="/medialive/%s" % (ps_name), Description=ps_description, Value=ps_value, Type='SecureString')
            print("DEBUG: Create Response:", reponse)
        else:
            print("Parameter Store entry '{0}' exists".format(ps_name))
            print("implement reveert steps here...")
    except e:
        if 'ParameterAlreadyExists' in e.message:
            print("Parameter Store entry '{0}' already exists".format(ps_name))
        else:
            print("unknown exception - message", repr(e.message))


def lambda_handler(event):
    # for local execution, the profile is used to grant permissions for the AWS requests
    profile = boto3.session.Session(profile_name)
    ssm = profile.client('ssm', region_name='us-west-2')
    package = profile.client('mediapackage', region_name='us-west-2')
    ID = event['ID']
    # create package endpoint
    package_destination = create_mediapackage(package, ID)
    playable_url = create_package_endpoint(package, ID)
    # create parameter store entries for push to MediaPackage
    response = create_param_store_entry(
        ssm, package_destination[0]['Username'],
        package_destination[0]['Password'], ps_description='later')
    response = create_param_store_entry(
        ssm, package_destination[1]['Username'],
        package_destination[1]['Password'], ps_description='later')
    # and package them nicely
    package_creds = {
        'Username': package_destination[0]['Username'],
        'Password': package_destination[0]['Password'],
        'URL': package_destination[0]['Url'],
        'Username2': package_destination[1]['Username'],
        'Password2': package_destination[1]['Password'],
        'URL2': package_destination[1]['Url'],
    }
    # The credentials package is needed for creating a MediaLive channel
    return package_creds


print(lambda_handler(event))
