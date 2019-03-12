import boto3

# input =
# {
#       "ID":                   'ID for the channel',
#       "input_type":           'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' |
#                               'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'
#       "source_urls":          ["list of", "source urls"]
#       'bitrate':              'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'
#       'resolution':           'SD' | 'HD' | 'UHD'
#       'mediaconnect_flows':    ["list of", "mediaconnectflows"],
# }

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


profile = boto3.session.Session()
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
