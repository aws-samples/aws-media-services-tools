# RTMP Streaming with the Videon Greylock and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Videon Greylock](#4-configure-the-videon-greylock)


### 4. Configure the Videon Greylock
- Videon Greylock [product documentation](https://streaming.videon-central.com/greylock/)
- Videon Greylock [product manual pdf](./Videon_Greylock_Sonora_Manual_20180824.pdf)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```
Configure the Videon Greylock using the parameters below:
Parameter | Notes
------------ | -------------
Protocol | RTMP
URL | rtmp://[ip address 1]:1935/[channel id]-1
