import boto3

'''
How to use:
Modify the event and profile variable definitions and execute the script
python3 ./Create_MediaPackage_Channel.py

What does it do:
This script will create a MediaLive Input, one of two prerequisies for
creating a MediaLive Channel.

Dependencies:
This script assumes an AWS CLI profile is avilable on the system it runs on.
For information about setting up local authentication:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

Inputs:
Expects an input dictionary as follows
input =
{
      "ID":                   'ID for the channel',
      "input_type":           'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' |
                              'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'
      "source_urls":          ["list of", "source urls"]
      'bitrate':              'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'
      'resolution':           'SD' | 'HD' | 'UHD'
      'mediaconnect_flows':    ["list of", "mediaconnectflows"],
}
'''

profile_name = 'the AWS CLI profile to use while creating MediaLive Resources'

input = {
    "ID": "test channel",
    "input_type": "RTMP_PUSH",
    "bitrate": "MAX_20_MBPS",
    "resolution": "HD"
}

# # create a rtp push MediaLive input
def rtp_push(client, Id, sg):
    response = client.create_input(
        Type="RTP_PUSH",
        InputSecurityGroups=[sg],
        Name=Id
    )
    return response

# Deprecated
# create the udp push (legacy) input
# def udp_push(client, Id, sg):
#     response = client.create_input(
#         Type="UDP_PUSH",
#         InputSecurityGroups=[sg],
#         Name=Id
#     )
#     return response

# create a rtmp pull MediaLive input
def rtmp_pull(client, Id, sg, source_a, source_b):
    response = client.create_input(
        Type="RTMP_PULL",
        InputSecurityGroups=[sg],
        Name=Id,
        Sources=[
            {'Url': source_a},
            {'Url': source_b},
        ]
    )
    return response

# create a rtmp push MediaLive input
def rtmp_push(client, Id, sg):
    response = client.create_input(
        Type="RTMP_PUSH",
        InputSecurityGroups=[sg],
        Destinations=[
            {'StreamName': "%s-1" % Id},
            {'StreamName': "%s-2" % Id}],
        Name=Id)
    return response

# create a url pull MediaLive input
def url_pull(client, Id, sg, source_a, source_b):
    response = client.create_input(
        Type="URL_PULL",
        InputSecurityGroups=[sg],
        Name=Id,
        Sources=[
            {'Url': source_a},
            {'Url': source_b},
        ]
    )
    return response

# create a MP4 file MediaLive input
def mp4_file(client, Id, sg, input_url_a, input_url_b):
    response = client.create_input(
        Type="MP4_FILE",
        InputSecurityGroups=[sg],
        Name=Id,
        Sources=[
            {'Url': input_url_a},
            {'Url': input_url_b}
        ]
    )
    return response

# create a MediaConnect input for MediaLive
def mediaconnect(client, Id, sg, flows, arn):
    response = client.create_input(
        Type="MEDIACONNECT",
        MediaConnectFlows = flows,
        InputSecurityGroups=[sg],
        Name=Id,
        RoleArn=arn
    )
    return response

# validates that a pull-based inputs have exactly two sources defined.
# returns a properly formatted list of source urls
def url_validator(input):
    try:
        urls = input['source_urls']
        if len(urls) == 0:
            print("No Sources defined, exiting now")
            exit(1)
        elif len(urls) != 2:
            if len(urls) >= 2:
                del urls[2:]
            urls.append(urls[0])
    except KeyError:
        print("No Source URLs provided, with input, exiting now")
        exit(1)
    return urls


# validates that a MEDIACONNECT input has MediaConnect flows defined for it.
# returns properly formatted MediaConnect flow ARNs
def media_connect_validator(input):
    try:
        flows = input['mediaconnectflows']
        if len(flows) > 2:
            print("Too many MediaConnect flows provided, only using the first two")
            del flows[2:]
        elif len(flows) == 0:
            print("No MediaConnect flows provided, exiting now")
            exit(1)
    except KeyError:
        print("No MediaConnect Flows provided, with mediaconnect input, exiting now")
        exit(1)
    out = []
    for x in flows:
        out.append({"FlowArn": x})
    return out

# TODO: replace with better code for providing an input security group
# or force the creation of a new Input security group each time
def input_sg(client):
    try:
        response = client.list_input_security_groups()['InputSecurityGroups']
        return response[0]['Id']
    except KeyError:
        response = client.create_input_security_group(
            WhitelistRules=[
                {"Cidr": "0.0.0.0/0"}
            ])
        return response['SecurityGroup']['Id']



profile = boto3.session.Session(profile_name=profile_name)
live = profile.client('medialive', region_name='us-west-2')

ID = input['ID']
arn = input['medialive_arn']

# create the specified input
if ['input_type'] == 'RTP_PUSH':
    input = rtp_push(live, ID, input_sg(live))
    destinations = input['Input']['Destinations']

elif input['input_type'] == 'RTMP_PUSH':
    input = rtmp_push(live, ID, input_sg(live))
    destinations = input['Input']['Destinations']

elif input['input_type'] == 'RTMP_PULL':
    urls = url_validator(input)
    input = rtmp_pull(live, ID, input_sg(live), urls[0], urls[1])
    sources = input['Input']['Sources']

elif input['input_type'] == 'URL_PULL':
    urls = url_validator(input)
    input = url_pull(live, ID, input_sg(live), urls[0], urls[1])
    sources = input['Input']['Sources']

elif input['input_type'] == 'MP4_FILE':
    urls = url_validator(input)
    input = mp4_file(live, ID, input_sg(live), urls[0], urls[1])
    sources = input['Input']['Sources']

elif input['input_type'] == 'MEDIACONNECT':
    flows = media_connect_validator(input)
    input = mediaconnect(live, ID, input_sg(live), input['mediaconnect_flows'], arn)

else:
    print("No valid input type specified, exiting now")
    exit(1)
input_id = input['Input']['Id']

# prints the input_id, which is necessary to create the MediaLive Channel
print(input_id)
