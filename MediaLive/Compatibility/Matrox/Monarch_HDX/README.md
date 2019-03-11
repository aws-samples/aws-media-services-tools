# RTMP Streaming with Matrox Monarch HD and AWS MediaLive
How to connect Elemental Live to a MediaLive channel using RTMP Push
1. [Create a MediaLive Input](#1-create-the-medialive-input)
2. [Create a MediaPackage Channel for playback](#2-create-a-mediapackage-channel-for-playback-of-the-medialive-stream)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure Monarch HDX](#4-configure-monarch-hdx)


### 4. Configure Monarch HDX
- Matrox software [Product Documentation](https://www.matrox.com/video/en/support/downloads/)
- Full documentation for the [Monarch HDX](https://www.matrox.com/video/en/support/downloads/download/?id=225&product=113&osName=28&productName=monarch_hdx&downloadType=Documentation)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```
Take the inputs below and substitute their values into the streamParam configuration blocks in the [MonarchHDX_Settings.xml](./MonarchHDX_Settings.xml)

Parameter | Notes
------------ | -------------
rtmpDestinationURL | rtmp://[ip address 1]:1935/hdx
rtmpStreamName | [channel id]-1
rtmpDestinationURL | rtmp://[ip address 2]:1935/hdx2
rtmpStreamName | [channel id]-2
Load the resultant XML

### Notes
:one: Valid MediaLive Input values are: `'RTP_PUSH' | 'RTMP_PUSH' | 'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE' | 'MEDIACONNECT'`<br>
:two: This parameter is only needed for the following input types: `'RTMP_PULL' | 'URL_PULL' | 'MP4_FILE'` <br>
:three: Valid Bitrate values are: `'MAX_10_MBPS' | 'MAX_20_MBPS' | 'MAX_50_MBPS'` <br>
:four: Valid Resolution values are: `'SD' | 'HD' | 'UHD'` <br>
:five: See [MediaConnect Flow Creation](http://github.com/kulpbenamazon/MediaConnect') and (link to aws website) for more MediaConnect information <br>
