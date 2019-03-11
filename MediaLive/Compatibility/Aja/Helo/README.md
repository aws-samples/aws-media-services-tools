# RTMP Streaming with Aja Helo and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Aja Helo](#4-configure-the-aja-helo)


### 4. Configure the Aja Helo
Aja Helo [product information](https://www.aja.com/products/helo)
Aja Helo [Manual PDF](https://github.com/aws-samples/aws-media-services-tools/tree/master/MediaLive/Compatibility/Aja/Helo/AJA_HELO_Manual_v1.1r1.pdf)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address]:1935/[channel id]-1
rtmp://[ip address]:1935/[channel id]-2
```

Create a streaming profile that uses the following parameters:
Parameter | Notes
------------ | -------------
Stream Type | RTMP
RTMP Server URL | rtmp://[Ip Address]:/[Channel Id]-1
RTMP Stream Name | helo
