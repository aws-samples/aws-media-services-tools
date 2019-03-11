# RTMP Streaming with the VITEC MGW Ace  and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the MGW Ace](#4-configure-the-mgw-ace)


### 4. Configure the MGW Ace
- MGW Ace [product documentation](https://www.vitec.com/products/encoders/portable-encoders/product/show/mgw-ace/)
- MGW Ace [API documentation](./MGW_Ace_Encoder_HTTP_API_v2.1.0.pdf)
- MGW Ace [product manual](./MGW_ACE_Encoder_User_Manual_v2.1_RevC.pdf)
The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```

Select the channels option on the left side product menu, see [screen capture 1](./MGW_Ace_Encoder_H264_RTMP.jpg) and [screen capture 2](./MGW_Ace_Encoder_HEVC_RTP_FEC.jpg) for reference.  Enter the parameters below in the target 1 and target 2 fields, respectively.
Parameter | Notes
------------ | -------------
Channel Name | vitec-1
Streaming Protocol | RTMP
Target Address | [ip address 1]
Target Port | 1935
Channel Name | vitec-2
Streaming Protocol | RTMP
Target Address | [ip address 2]
