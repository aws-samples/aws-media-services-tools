# RTMP Streaming with Zixi On Air and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure Zixi On Air](#4-configure-zixi-on-air)


### 4. Configure Zixi On Air
- Zixi On Air [product info](https://www.zixi.com/applications-on-air)
- Zixi On Air [App Store Link](https://itunes.apple.com/us/developer/zixi/id1279219968) [Google Play Link](https://play.google.com/store/apps/developer?id=Zixi)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```

Open the Settings page and enter the parameters below:
Parameter | Notes
------------ | -------------
Protocol | RTMP
URL | rtmp://[ip address 1]:1935/
Stream Key | [channel_id]-1
