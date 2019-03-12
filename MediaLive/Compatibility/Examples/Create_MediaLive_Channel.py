import boto3
# import random
#
#
# assumes Lambda event input in json format like:
#
# { "input": {
#       "TEST_ID":              "ID for the test",
#       "input_type":                 'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' |
#                               'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'
#       "endpoint":             <Only includeded with pull inputs>,
#       "source_urls":          ["list of", "source urls"]
#       'bitrate':              'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'
#       'resolution':           'SD' | 'HD' | 'UHD'
#       'mediaconnectflows':    ["list of", "mediaconnectflows"],
#       'medialivearn':         "the arn for the role MediaLive uses"
# }
#
###                   ###
###  TEST RESOURCES   ###
#
# uncomment the following to test locally instead of in Lambda
# TEST_ID="test-id-%s" % (str(random.randint(100,900)))
#
# event = {
#     "input": {
#         "TEST_ID": "%s" % TEST_ID,
#         "type": 'MP4_FILE',
#         "bitrate": "MAX_20_MBPS",
#         "resolution": "HD",
#         "destination": "s3://bluegill-output/%s/" % TEST_ID,
#         "source_urls": ["http://sumbplace.com/file.mp4"],
#         "mediaconnectflows": ["arn:aws:mediaconnect:us-west-2:657276638238:flow:1-VwBYDQYBVwUGVANZ-968954869347:test"],
#         "medialivearn": "arn:aws:iam::657276638238:role/MediaLiveAccessRole"
#     }
# }


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


# creates the MediaLive channel using the input created and using a large
# bock of boilerplate encoder settings
def create_channel(client, input_id, destination, ID, event, arn):
    # the input_id is just the ID of the input we dynamically create earlier
    #
    # the first destination should always follow the pattern:
    # s3://bluegill-output/TEST_ID/
    #
    # the second destination, which gets passed into the function
    # should always be a dynamically created
    # mediapackage endpoint for showing playback
    #
    # If you're extending this function for some non-bluegill usage, you'll
    # want to provide  a way of passing in the correct destinations for MediaLive
    response = client.create_channel(
        Destinations=[{
            'Id': "%s-s3" % ID,
            'Settings': [
                {
                    'Url': "s3://bluegill-output/%s/output" % ID
                },
                {
                    'Url': "s3://bluegill-output/junkdrawer/output"
                }
            ]
        },
         {
             'Id': "%s-mp" % ID,
             'Settings': [
                 {
                     'Url': destination['URL'],
                     'Username': destination['Username'],
                     'PasswordParam': "/medialive/%s" % destination['Username']
                 },
                 {
                     'Url': destination['URL2'],
                     'Username': destination['Username2'],
                     'PasswordParam': "/medialive/%s" % destination['Username2']
                 },
             ]
         }],
        InputAttachments=[{
            "InputId": input_id
        }],
        EncoderSettings={
        "TimecodeConfig": {
            "Source": "SYSTEMCLOCK"
        },
        "OutputGroups": [
            {
                "OutputGroupSettings": {
                    "HlsGroupSettings": {
                        "TimedMetadataId3Frame": "PRIV",
                        "CaptionLanguageMappings": [],
                        "Destination": {
                            "DestinationRefId": "%s-s3" % ID,
                        },
                        "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                        "IndexNSegments": 7,
                        "InputLossAction": "EMIT_OUTPUT",
                        "ManifestDurationFormat": "FLOATING_POINT",
                        "CodecSpecification": "RFC_4281",
                        "IvInManifest": "INCLUDE",
                        "TimedMetadataId3Period": 2,
                        "ProgramDateTimePeriod": 2,
                        "SegmentLength": 10,
                        "CaptionLanguageSetting": "OMIT",
                        "ProgramDateTime": "INCLUDE",
                        "HlsCdnSettings": {
                            "HlsBasicPutSettings": {
                                "ConnectionRetryInterval": 1,
                                "FilecacheDuration": 300,
                                "NumRetries": 10
                            }
                        },
                        "TsFileMode": "SEGMENTED_FILES",
                        "StreamInfResolution": "INCLUDE",
                        "ClientCache": "ENABLED",
                        "AdMarkers": [
                            "ELEMENTAL_SCTE35"
                        ],
                        "KeepSegments": 360,
                        "SegmentationMode": "USE_SEGMENT_DURATION",
                        "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                        "ManifestCompression": "NONE",
                        "DirectoryStructure": "SINGLE_DIRECTORY",
                        "Mode": "LIVE"
                    }
                },
                "Outputs": [
                    {
                        "VideoDescriptionName": "video_1080p30",
                        "AudioDescriptionNames": [
                            "audio_1"
                        ],
                        "CaptionDescriptionNames": [],
                        "OutputSettings": {
                            "HlsOutputSettings": {
                                "NameModifier": "_1080p30",
                                "HlsSettings": {
                                    "StandardHlsSettings": {
                                        "M3u8Settings": {
                                            "PcrControl": "PCR_EVERY_PES_PACKET",
                                            "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                            "PmtPid": "480",
                                            "Scte35Pid": "500",
                                            "VideoPid": "481",
                                            "ProgramNum": 1,
                                            "AudioPids": "492-498",
                                            "AudioFramesPerPes": 4,
                                            "EcmPid": "8182",
                                            "Scte35Behavior": "PASSTHROUGH"
                                        },
                                        "AudioRenditionSets": "PROGRAM_AUDIO"
                                    }
                                }
                            }
                        }
                    }
                ],
                "Name": "S3"
            },
            {
                "OutputGroupSettings": {
                    "HlsGroupSettings": {
                        "TimedMetadataId3Frame": "PRIV",
                        "CaptionLanguageMappings": [],
                        "Destination": {
                            "DestinationRefId": "%s-mp" % ID
                        },
                        "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                        "IndexNSegments": 7,
                        "InputLossAction": "EMIT_OUTPUT",
                        "ManifestDurationFormat": "FLOATING_POINT",
                        "CodecSpecification": "RFC_4281",
                        "IvInManifest": "INCLUDE",
                        "TimedMetadataId3Period": 1,
                        "ProgramDateTimePeriod": 1,
                        "SegmentLength": 10,
                        "CaptionLanguageSetting": "OMIT",
                        "ProgramDateTime": "INCLUDE",
                        "Mode": "LIVE",
                        "TsFileMode": "SEGMENTED_FILES",
                        "StreamInfResolution": "INCLUDE",
                        "ClientCache": "ENABLED",
                        "AdMarkers": [],
                        "KeepSegments": 40,
                        "SegmentationMode": "USE_SEGMENT_DURATION",
                        "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                        "ManifestCompression": "NONE",
                        "DirectoryStructure": "SINGLE_DIRECTORY",
                        "HlsCdnSettings": {
                            "HlsBasicPutSettings": {
                                "ConnectionRetryInterval": 1,
                                "FilecacheDuration": 300,
                                "NumRetries": 10
                            }
                        }
                    }
                },
                "Outputs": [
                    {
                        "OutputName": "vf6z8",
                        "AudioDescriptionNames": [
                            "audio_f42hdc"
                        ],
                        "CaptionDescriptionNames": [],
                        "VideoDescriptionName": "video_tikzx7",
                        "OutputSettings": {
                            "HlsOutputSettings": {
                                "SegmentModifier": "$dt$",
                                "NameModifier": "_1",
                                "HlsSettings": {
                                    "StandardHlsSettings": {
                                        "M3u8Settings": {
                                            "PcrControl": "PCR_EVERY_PES_PACKET",
                                            "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                            "PmtPid": "480",
                                            "Scte35Pid": "500",
                                            "VideoPid": "481",
                                            "ProgramNum": 1,
                                            "AudioPids": "492-498",
                                            "AudioFramesPerPes": 4,
                                            "EcmPid": "8182",
                                            "Scte35Behavior": "NO_PASSTHROUGH"
                                        },
                                        "AudioRenditionSets": "PROGRAM_AUDIO"
                                    }
                                }
                            }
                        }
                    }
                ],
                "Name": "MediaPackage"
            }
        ],
        "GlobalConfiguration": {
            "SupportLowFramerateInputs": "DISABLED",
            "OutputTimingSource": "SYSTEM_CLOCK",
            "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
        },
        "CaptionDescriptions": [],
        "VideoDescriptions": [
            {
                "CodecSettings": {
                    "H264Settings": {
                        "Syntax": "DEFAULT",
                        "FramerateNumerator": 30,
                        "Profile": "HIGH",
                        "GopSize": 2,
                        "AfdSignaling": "NONE",
                        "FramerateControl": "SPECIFIED",
                        "ColorMetadata": "INSERT",
                        "FlickerAq": "ENABLED",
                        "LookAheadRateControl": "HIGH",
                        "FramerateDenominator": 1,
                        "Bitrate": 6000000,
                        "TimecodeInsertion": "PIC_TIMING_SEI",
                        "NumRefFrames": 3,
                        "EntropyEncoding": "CABAC",
                        "GopSizeUnits": "SECONDS",
                        "Level": "H264_LEVEL_AUTO",
                        "GopBReference": "ENABLED",
                        "AdaptiveQuantization": "HIGH",
                        "GopNumBFrames": 3,
                        "ScanType": "PROGRESSIVE",
                        "ParControl": "INITIALIZE_FROM_SOURCE",
                        "Slices": 1,
                        "SpatialAq": "ENABLED",
                        "TemporalAq": "ENABLED",
                        "RateControlMode": "CBR",
                        "SceneChangeDetect": "ENABLED",
                        "GopClosedCadence": 1
                    }
                },
                "Name": "video_1080p30",
                "Sharpness": 50,
                "Height": 1080,
                "Width": 1920,
                "ScalingBehavior": "DEFAULT",
                "RespondToAfd": "NONE"
            },
            {
                "CodecSettings": {
                    "H264Settings": {
                        "Syntax": "DEFAULT",
                        "Profile": "MAIN",
                        "GopSize": 1,
                        "AfdSignaling": "NONE",
                        "FramerateControl": "SPECIFIED",
                        "FramerateNumerator": 30,
                        "FramerateDenominator": 1,
                        "ColorMetadata": "INSERT",
                        "FlickerAq": "ENABLED",
                        "LookAheadRateControl": "MEDIUM",
                        "Bitrate": 2000000,
                        "TimecodeInsertion": "PIC_TIMING_SEI",
                        "NumRefFrames": 1,
                        "EntropyEncoding": "CABAC",
                        "GopSizeUnits": "SECONDS",
                        "Level": "H264_LEVEL_AUTO",
                        "GopBReference": "DISABLED",
                        "AdaptiveQuantization": "MEDIUM",
                        "GopNumBFrames": 0,
                        "ScanType": "PROGRESSIVE",
                        "ParControl": "INITIALIZE_FROM_SOURCE",
                        "SpatialAq": "ENABLED",
                        "TemporalAq": "ENABLED",
                        "RateControlMode": "CBR",
                        "SceneChangeDetect": "ENABLED",
                        "GopClosedCadence": 1
                    }
                },
                "Name": "video_tikzx7",
                "Sharpness": 50,
                "Height": 540,
                "Width": 960,
                "ScalingBehavior": "DEFAULT",
                "RespondToAfd": "NONE"
            }
        ],
        "AudioDescriptions": [
            {
                "CodecSettings": {
                    "AacSettings": {
                        "Profile": "LC",
                        "InputType": "NORMAL",
                        "RateControlMode": "CBR",
                        "Spec": "MPEG4",
                        "SampleRate": 48000,
                        "Bitrate": 128000,
                        "CodingMode": "CODING_MODE_2_0",
                        "RawFormat": "NONE"
                    }
                },
                "LanguageCode": "eng",
                "AudioSelectorName": "Default",
                "LanguageCodeControl": "USE_CONFIGURED",
                "AudioTypeControl": "USE_CONFIGURED",
                "AudioType": "UNDEFINED",
                "Name": "audio_1"
            },
            {
                "CodecSettings": {
                    "AacSettings": {
                        "Profile": "LC",
                        "InputType": "NORMAL",
                        "RateControlMode": "CBR",
                        "Spec": "MPEG4",
                        "SampleRate": 48000,
                        "Bitrate": 192000,
                        "CodingMode": "CODING_MODE_2_0",
                        "RawFormat": "NONE"
                    }
                },
                "LanguageCodeControl": "FOLLOW_INPUT",
                "AudioTypeControl": "FOLLOW_INPUT",
                "Name": "audio_f42hdc",
                "AudioSelectorName": "audio_f42hdc"
            }
        ]
        },
        Name=ID,
        RoleArn=arn
    )
    return response

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

# checks to see if there's already a security group that MediaLive can use,
# if one is present, it is used, if not, one is created
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

# # create a rtp push MediaLive input
def rtp_push(client, Id, sg):
    response = client.create_input(
        Type="RTP_PUSH",
        InputSecurityGroups=[sg],
        Name=Id
    )
    return response

# create the udp push (legacy) input, hence it's commented out
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

# update the dynamodb Resources table to include the resources created
def update_resources_table(client, input_id, Id, ml_channel_id):
    response = client.put_item(
        TableName="RESOURCES",
        Item={
          'TEST_ID': {'S': Id},
          'MediaLiveInput': {'S': input_id},
          'MediaPackageEndpoint': {'S': Id},
          'MediaLiveChannel': {'S': ml_channel_id},
          'MediaPackageChannel': {'S': Id}
          })


# The default Lambda Handler
def lambda_handler(event, context):
    # create clients based on the specified profile these are used for local testing
    # ben = boto3.session.Session(profile_name='ben')
    # live = ben.client('medialive', region_name='us-west-2')
    # package = ben.client('mediapackage', region_name='us-west-2')
    # ssm = ben.client('ssm', region_name='us-west-2')
    # data = ben.client('dynamodb', region_name='us-west-2')
    #
    # The clients initiated below are for production lambda usage and
    # assum the AWS SECET KEY, etc are provided as environment variables
    # in the lambda runtime.
    #
    profile = boto3.session.Session(profile_name=profile_name)
    live = profile.client('medialive', region_name='us-west-2')
    package = profile.client('mediapackage', region_name='us-west-2')
    ssm = profile.client('ssm', region_name='us-west-2')

    ID = event['TEST_ID']
    arn = event['medialivearn']
    destinations = ""
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
    # create the specified input
    if event['input_type'] == 'RTP_PUSH':
        input = rtp_push(live, ID, input_sg(live))
        destinations = input['Input']['Destinations']

    elif event['input_type'] == 'RTMP_PUSH':
        input = rtmp_push(live, ID, input_sg(live))
        destinations = input['Input']['Destinations']

    elif event['input_type'] == 'RTMP_PULL':
        urls = url_validator(event)
        input = rtmp_pull(live, ID, input_sg(live), urls[0], urls[1])
        sources = input['Input']['Sources']

    elif event['input_type'] == 'URL_PULL':
        urls = url_validator(event)
        input = url_pull(live, ID, input_sg(live), urls[0], urls[1])
        sources = input['Input']['Sources']

    elif event['input_type'] == 'MP4_FILE':
        urls = url_validator(event)
        input = mp4_file(live, ID, input_sg(live), urls[0], urls[1])
        sources = input['Input']['Sources']

    elif event['input_type'] == 'MEDIACONNECT':
        flows = media_connect_validator(event)
        input = mediaconnect(live, ID, input_sg(live), flows, arn)

    else:
        print("No valid input type specified, exiting now")
        exit(1)
    input_id = input['Input']['Id']
    print(input_id)
    # acutally create the channel
    response = create_channel(live, input_id, package_creds, ID, event, arn)['Channel']['Id']
    update_resources_table(data, input_id, ID, response)
    output = {}
    output["Destinations"] = destinations
    output["PlaybackUrl"]  = playable_url
    output["TEST_ID"] = ID
    return event


###             ###
### Test Code   ###
#
# uncomment to test locally
#
# context="stringy"
# lambda_handler(event['input'], context)
