# RTMP Streaming with the Z3 Technology DME-20 and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the DME-20](#4-configure-the-dme-20)


### 4. Configure the DME-20
The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```

Under the Output Setup section, enter the parameters below [image for reference](./DME-20.png).
Parameter | Notes
------------ | -------------
Output Format | RTMP
Aux File Enable | None
Dest Address | [ip address 1]/dme-20/[channel id]-1
