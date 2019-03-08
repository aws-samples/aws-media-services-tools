import boto3


## TODO: example input in comments,
## Lambda Handler wrapper
## how to use Instructions

input = {
    "ID": "test channel",
    "input_type": "RTMP_PUSH",
    "bitrate": "MAX_20_MBPS",
    "resolution": "HD"
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

def lambda_handler(event, context):
