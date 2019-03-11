# RTMP Streaming with Epiphan Pearl Mini and AWS MediaLive
How to connect Elemental Live to a MediaLive channel using RTMP Push
1. [Create a MediaLive Input](#1-create-the-medialive-input)
2. [Create a MediaPackage Channel for playback](#2-create-a-mediapackage-channel-for-playback-of-the-medialive-stream)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure the Pearl Mini](#4-configure-the-pearl-mini)


### 4. Configure the Pearl Mini
The MediaLive input creation will provide two input URLs with the following structure:
```
rtmp://[ip address]/[channel id]-1
rtmp://[ip address]/[channel id]-2
```
Use the provided [pdf directions](./pearl-StreamingGuide-amazon-4-7-1.pdf) to configure the Pearl Mini.
