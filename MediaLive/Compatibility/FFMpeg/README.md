# RTMP Streaming with FFmpeg and AWS MediaLive
How to connect Elemental Live to a MediaLive channel using RTMP Push
1. [Create a MediaLive Input](#1-create-the-medialive-input)
2. [Create a MediaPackage Channel for playback](#2-create-a-mediapackage-channel-for-playback-of-the-medialive-stream)
3. [Create the MediaLive Channel](#3-create-the-medialive-channel)
4. [Configure FFmpeg](#4-configure-ffmpeg)


### 4. Configure FFmpeg
Following the detailed directions [here](https://d1.awsstatic.com/awselemental/workflowexamples/Workflow4_Example_FFMPEG_RTMP_to_MediaLive_and_MediaPackage.pdf) using the inputs the provided by MediaLive below.
```
rtmp://[ip address 1]:1935/[channel id]-1
rtmp://[ip address 2]:1935/[channel id]-2
```
