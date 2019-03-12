# RTMP Streaming with AJA HELO and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the AJA HELO](#4-configure-the-aja-helo)


## Detailed Instructions and Examples
An AWS Elemental MediaLive channel has two dependencies, an input and an output.  The example code below will create a MediaLive input and will use a HLS output to an AWS Elemental MediaPackage channel.  For a full list of possible outputs, see the MediaLive documentation available [here](https://docs.aws.amazon.com/medialive/latest/ug/creating-a-channel-step5.html).
### 1. Create an AWS Elemental MediaLive input
##### To create the MediaLive input, use either the Python script or AWS Lambda-optimized code below
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
medialive_arn | The ARN for the IAM role that the MediaLive channel will use
##### Both scripts will return the MediaLive Input ID, note the value, because it is needed to create the MediaLive Channel


### 2. Create an AWS Elemental MediaPackage channel
##### To create the MediaPackage channel for stream playback, use either the Python script or AWS Lambda-optimized code below
- [Create_MediaPackage_Channel.py](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/Create_MediaPackage_Channel.py)
- [Create MediaPackage Lambda](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/Lambda_Create_MediaPackage_Channel.py)
- [Example Input JSON](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaPackage/Compatibility/Examples/MediaPackage_Channel.json)
##### Both scripts expect an input dictionary that contains the following information
Parameter | Notes
------------ | -------------
ID | A unique name for the MediaPackage resources
##### Both scripts will return a JSON data structure with the MediaPackage destination information, note the values, because they will be needed to create the MediaLive channel


### 3. Create the MediaLive Channel
##### To create the MediaLive channel, use either the Python script or AWS Lambda-optimized code below
- [Create_MediaLive_Channel.py](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Create_MediaLive_Channel.py)
- [MediaLive Channel Lambda](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples/Lambda_Create_MediaLive_Channel.py)
- [Example MediaLive channel creation JSON](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Examples//MediaLive_Input.json)
##### Both scripts expect an input data structure that contains the following information
Parameter | Notes
------------ | -------------
ID | a unique name for the MediaLive resources
input_id | the output of the MediaLive input creation
destination_id | the output of the MediaPackage channel creation


### 4. Configure the AJA HELO
- AJA HELO [product information](https://www.aja.com/products/helo)
- AJA HELO [Manual PDF](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Aja/Helo/AJA_HELO_Manual_v1.1r1.pdf)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```

Create a streaming profile that uses the following parameters:
Parameter | Notes
------------ | -------------
Stream Type | RTMP
RTMP Server URL | rtmp://[ip address 1]:/[channel id]-1
RTMP Stream Name | HELO


### Notes
:one: Valid MediaLive input values are: `'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'`<br>
:two: This parameter is only needed for the following input types: `'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE'` <br>
:three: Valid bitrate values are: `'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'` <br>
:four: Valid resolution values are: `'SD' | 'HD' | 'UHD'` <br>
:five: See [MediaConnect Flow Creation](http://github.com/aws-samples/aws-media-services-tools/tree/master/MediaConnect/Compatibility/Examples/') and [MediaConnect Product Information](https://aws.amazon.com/mediaconvert/) for more information on using AWS Elemental MediaConnect <br>
