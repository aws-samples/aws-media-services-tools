import boto3


'''
How to use:
Modify the event and profile variable definitions and execute the script
python3 ./Create_MediaLive_Channel.py

What does it do:
This script will create a MediaLive Channel, it has two prerequisites: a
MediaLive Input, which is where video will originate from and a MediaPackage
Destination, where the video will be delivered.

Dependencies:
This script assumes an AWS CLI profile is avilable on the system it runs on.
For information about setting up local authentication:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
It also expects a IAM RoleArn that the MediaLive Channel will use.

Inputs:
The input_id and destination_id can be created using these scripts:
https://github.com/aws-samples/aws-media-services-tools/blob/master/MediaPackage/Compatibility/Examples/Create_MediaPackage_Channel.py
https://github.com/aws-samples/aws-media-services-tools/blob/master/MediaLive/Compatibility/Examples/Create_MediaLive_Input.py
The medialive_arn should be created in the AWS console following this documentation:
https://docs.aws.amazon.com/medialive/latest/ug/role-and-remember-arn.html
input = {
    'ID': 'test channel',
    'input_id': 'the output of the MediaLive Input creation script',
    'destination_id': {
        'Username':  'user 1',
        'Password':  'credentials',
        'URL':       'destination url 1',
        'Username2': 'user 2',
        'Password2': 'credentials',
        'URL2':      'destination url 2',
    },
    'medialive_arn': 'Arn::'
}
'''
profile_name = 'Valid AWS CLI profile'
input = {
}

# creates the MediaLive channel using the input created and using a large
# block of boilerplate encoder settings
def create_channel(client, input_id, destination, ID, event, arn):
    response = client.create_channel(
        Destinations=[
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
                            "DestinationRefId": "%s-mp" % ID,
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
        RoleArn=arn)
    return response


# The default Lambda Handler
def lambda_handler(event):
    # creates a client using the specified profile
    profile = boto3.session.Session(profile_name=profile_name)
    live = profile.client('medialive', region_name='us-west-2')
    ID = event['ID']
    arn = event['medialive_arn']
    input_id = event['input_id']
    package_creds = event['destination_id']
    # create the channel
    response = create_channel(live, input_id, package_creds, ID, event, arn)['Channel']['Id']
    return response

print(lambda_handler(input))
