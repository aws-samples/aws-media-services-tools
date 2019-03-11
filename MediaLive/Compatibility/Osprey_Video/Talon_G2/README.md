# RTMP Streaming with the Talon G2 and AWS MediaLive
How to connect AWS Elemental Live to an AWS Elemental MediaLive channel using RTMP Push
1. [Create an AWS Elemental MediaLive Input](#1-create-an-aws-elemental-medialive-input)
2. [Create an AWS Elemental MediaPackage Channel](#2-create-an-aws-elemental-mediapackage-channel)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Talon G2](#4-configure-the-talon-g2)


### 4. Configure the Talon G2
- Osprey Talon G2 [product page](https://www.ospreyvideo.com/images/osprey/datasheets/Talon_Encoder_Specs.pdf)
- Osprey Talon G2 [API guide](./Talon_Encoder_API_1_10_0_250.pdf)
- Osprey Talon G2 [user manual](./Talon_Encoder_User_Guide_2018_10.pdf)

The MediaLive input creation provides two input URLs with the following structure:
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```
Use those values to configure the Talon G2
