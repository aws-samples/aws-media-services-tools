# RTP Streaming with T400 and AWS MediaLive

How to connect Elemental Live to a MediaLive channel using RTP Push

1. [Create a MediaLive Input](#1-create-the-medialive-input)
2. [Create a MediaPackage Channel for playback](#2-create-a-mediapackage-channel-for-playback-of-the-medialive-stream)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure T400 Transcoder](#4-configure-t400)

## Detailed Instructions and Examples

An AWS Elemental MediaLive channel has two dependencies, an input and an output.  The example code below will create a MediaLive input and will use a HLS output to an AWS Elemental MediaPackage channel.  For a full list of possible outputs, see the MediaLive documentation available [here](https://docs.aws.amazon.com/medialive/latest/ug/creating-a-channel-step5.html).

### 1. Create an AWS Elemental MediaLive input

#### To create the MediaLive input, use either the Python script or AWS Lambda-optimized code below

- [Create_MediaLive_Input.py](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Create_MediaLive_Input.py)
- [MediaLive Input Lambda](https://github.com/kulpbenamazon/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Lambda_Create_MediaLive_Input.py)
- [Example RTMP_PUSH Input JSON](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/MediaLive_Input.json)

##### Both scripts expect an input dictionary that contains the following information

Parameter | Notes
------------ | -------------
ID | A unique name for the MediaLive resources
input_type | The type of MediaLive input that you are creating [:one:](#notes)
source_urls | An array of source URLs from which MediaLive will pull content [:two:](#notes)
bitrate | The expected bitrate of the stream [:three:](#notes)
resolution | The expected resolution of the stream [:four:](#notes)
mediaconnect_flows | An array of ARNs (Amazon Resource Names) for the AWS Elemental MediaConnect flows [:five:](#notes)

##### Both scripts will return the MediaLive Input ID, note the value, because it is needed to create the MediaLive Channel

### 2. Create an AWS Elemental MediaPackage channel

#### To create the MediaPackage channel for stream playback, use either the Python script or AWS Lambda-optimized code below

- [Create_MediaPackage_Channel.py](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/Create_MediaPackage_Channel.py)
- [Create MediaPackage Lambda](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/Lambda_Create_MediaPackage_Channel.py)
- [Example Input JSON](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/MediaPackage_Channel.json)

##### Both scripts expect an input dictionary that contains the following information

Parameter | Notes
------------ | -------------
ID | A unique name for the MediaPackage resources

##### Both scripts will return a JSON data structure with the MediaPackage destination information, note the values, because they will be needed to create the MediaLive channel

### 3. Create the MediaLive Channel

#### To create the MediaLive channel, use either the Python script or AWS Lambda-optimized code below

- [Create_MediaLive_Channel.py](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Create_MediaLive_Channel.py)
- [MediaLive Channel Lambda](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Lambda_Create_MediaLive_Channel.py)
- [Example MediaLive channel creation JSON](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/MediaLive_Channel.json)

##### Both scripts expect an input data structure that contains the following information

Parameter | Notes
------------ | -------------
ID | a unique name for the MediaLive resources
input_id | the output of the MediaLive input creation
destination_id | the output of the MediaPackage channel creation
medialive_arn | The ARN for the IAM role that the MediaLive channel will use

### 4. Configure T400 Transcoder

Configuration of the T400 Transcoder can be done through FFmpeg.
After MediaLive inputs have been setup, video can be transcoded through the T400 and sent via RTP to MediaLive using an FFmpeg command. Here is an example which uses RTP MediaLive inputs, **ip address 1** and **ip address 2**:

```sh
sudo ffmpeg -re -c:v h264_ni_dec -i videos/Compatibility-Program-Test-Source.mp4 \
-map 0 -c:v h265_ni_enc \
-xcoder-params "gopPresetIdx=5:intraPeriod=120:RcEnable=1:transRate=5000000:bitrate=4000000:repeatHeaders=1" \
-c:a aac -ac 2 -b:a 128k \
-f tee "[f=rtp_mpegts]rtp://[ip address 1]:5000/|[f=rtp_mpegts]rtp://[ip address 2]:5000/"
```

This example command will transcode an input h264 file into 4Mb/s h265 and send it via dual RTP connections to MediaLive. For further details regarding configuration of FFmpeg or T400 please refer to the [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html) or T400 IntegrationProgrammingGuide respectively.

### Notes

:one: Valid MediaLive input values are: `'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'`\
:two: This parameter is only needed for the following input types: `'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE'` \
:three: Valid bitrate values are: `'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'` \
:four: Valid resolution values are: `'SD' | 'HD' | 'UHD'` \
:five: See [MediaConnect Flow Creation](http://github.com/aws-samples/aws-media-services-tools/tree/master/MediaConnect/Compatibility/Examples/') and [MediaConnect Product Information](https://aws.amazon.com/mediaconvert/) for more information on using AWS Elemental MediaConnect
