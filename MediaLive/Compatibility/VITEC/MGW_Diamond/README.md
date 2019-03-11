# RTMP Streaming with the Vitec MGW Diamond  and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the MGW Diamond](#4-configure-the-mgw-Diamond)


### 4. Configure the MGW Diamond
- MGW Diamond [product documentation](https://www.vitec.com/products/encoders/portable-encoders/product/show/mgw-diamond)
- MGW Diamond [API documentation](./MGW_Diamond_TOUGH_V1.6_HTTPS_API.pdf)
- MGW Diamond [product manual](./MGW_Diamond_Encoder_User_Manual_v1.6_RevA.pdf)
The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```

Select the channels option on the left side product menu, and enter the parameters below in the target 1 and target 2 fields, respectively.
Parameter | Notes
------------ | -------------
Channel Name | vitec-1
Streaming Protocol | RTMP
Target Address | [ip address 1]
Target Port | 1935
Channel Name | vitec-2
Streaming Protocol | RTMP
Target Address | [ip address 2]
