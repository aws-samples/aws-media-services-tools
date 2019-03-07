# RTMP Streaming with Elemental Live and AWS MediaLive
How to connect Elemental Live to a MediaLive channel using RTMP Push
1. [Create a MediaLive Input](#1-create-the-medialive-input)
2. [Create a MediaPackage Channel for playback](#2-create-a-mediapackage-channel-for-playback-of-the-medialive-stream)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Boxcast Platform to push RTMP to MediaLive](#4-configure-the-boxcast-platform-to-push-to-the-medialive-input)
<br>

## Detailed Instructions and Examples
### 1. Create the MediaLive Input
##### Using the python script or AWS Lambda-optimized linked below
- [Create_MediaLive_Input.py](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/Create_MediaLive_Input.py)
- [MediaLive Input Lambda](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/Lambda_Create_MediaLive_Input.py)
- [Example RTMP_PUSH Input JSON](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/MediaLive_Input.json)
##### Both sets of code will return the MediaLive Input ID which is needed to create the MediaLive Channel
##### Both functions expect an input dictionary that contains the following information
Parameter | Notes
------------ | -------------
ID | A unique name for the MediaLive resources
input_type | The type of MediaLive Input you are attemting to create [:one:](#notes)
source_urls | An array of source urls from which MediaLive will pull content [:two:](#notes)
bitrate | The expected bitrate of the stream [:three:](#notes)
resolution | The expected resolution of the stream [:four:](#notes)
mediaconnect_flows | An array of MediaConnect Flow ARNs (Amazon Resource Names) [:five:](#notes)
medialive_arn | The ARN for the IAM Role that the MediaLive channel will use
<br>

### 2. Create a MediaPackage Channel for playback of the MediaLive stream
- [Create_MediaPackage_Channel.py](https://github.com/kulpbenamazon/demo/blob/master/MediaPackage/Compatibility/Examples/Create_MediaPackage_Channel.py)
- [Create MediaPackage Lambda](https://github.com/kulpbenamazon/demo/blob/master/MediaPackage/Compatibility/Examples/Lambda_Create_MediaPackage_Channel.py)
- [Example Input JSON](https://github.com/kulpbenamazon/demo/blob/master/MediaPackage/Compatibility/Examples/MediaPackage_Channel.json)
##### Both functions expect an input dictionary that contains the following information
Parameter | Notes
------------ | -------------
ID | a unique name for the MediaPackage resources
<br>

### 3. Create the MediaLive Channel
- [Create_MediaLive_Channel.py](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/Create_MediaLive_Channel.py)
- [MediaLive Channel Lambda](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/Lambda_Create_MediaLive_Channel.py)
- [Example MediaLive channel creation JSON](https://github.com/kulpbenamazon/demo/blob/master/MediaLive/Compatibility/Examples/MediaLive_Input.json)
##### Both functions expect an input dictionary that contains the following information
Parameter | Notes
------------ | -------------
ID | a unique name for the MediaLive resources
input_id | the output ID from the MediaLive Input creation
destination_id | the output dictionary from the MediaPackage channel creation
<br>

### 4. Configure the Boxcast Platform to push to the MediaLive Input
The MediaLive input creation will provide two input URLs with the following structure:
```
rtmp://[ip address]/[channel id]-1
rtmp://[ip address]/[channel id]-2
```
Use the provided [Boxcast Blog Post](https://boxcast.zendesk.com/hc/en-us/articles/360022974052-How-to-Broadcast-to-AWS-Elemental-MediaLive-via-BoxCast) to configure the Boxcast Platform. 

<br>

### Notes
:one: Valid MediaLive Input values are: `'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'`<br>
:two: This parameter is only needed for the following input types: `'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE'` <br>
:three: Valid Bitrate values are: `'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'` <br>
:four: Valid Resolution values are: `'SD' | 'HD' | 'UHD'` <br>
:five: See [MediaConnect Flow Creation](http://github.com/kulpbenamazon/MediaConnect') and (link to aws website) for more MediaConnect information <br>
