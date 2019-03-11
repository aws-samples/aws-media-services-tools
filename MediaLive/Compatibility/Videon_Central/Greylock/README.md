# RTMP Streaming with the Videon Central Greylock and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Greylock](#4-configure-the-greylock)


### 4. Configure the Greylock
- Greylock [product documentation](https://streaming.videon-central.com/greylock/)
- Greylock [product manual pdf](./Videon_Greylock_Sonora_Manual_20180824.pdf)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```
Configure the Greylock using the parameters below:
Parameter | Notes
------------ | -------------
Protocol | RTMP
URL | rtmp://[ip address 1]:1935/[channel id]-1
