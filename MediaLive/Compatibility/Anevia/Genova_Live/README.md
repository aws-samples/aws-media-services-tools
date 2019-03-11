# RTMP Streaming with Aja Helo and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Genova Live](#4-configure-the-genova-live)


### 4. Configure the Genova Live
The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address]:1935/[channel id]-1
rtmp://[ip address]:1935/[channel id]-2
```

Create a streaming profile that uses the following parameters:
Parameter | Notes
------------ | -------------
