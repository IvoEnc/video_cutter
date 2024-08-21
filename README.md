Video Cutter Application - User Manual

Overview

The Video Cutter Application is a simple tool that allows you to load a video file, select a segment by marking start and end points, and save the segment as a new video file. The application features a clean and easy-to-use interface built with PyQt5.

How to Use the Application
1. Open a Video File
Click the "Open File" button.
Select the video file you want to work with. The video will start playing automatically.

2. Play and Navigate the Video
The video starts playing as soon as you open a file.
You can navigate through the video using the arrow keys:
Left Arrow (←): Rewind the video by 5 seconds.
Right Arrow (→): Fast forward the video by 5 seconds.

3. Mark the Segment
Mark Start (1): Press the 1 key to mark the start of the segment.
Mark End (2): Press the 2 key to mark the end of the segment.

4. Save the Segment
Once both start and end points are marked, click the "Save" button.
The selected segment will be saved as a new video file in the same directory as the original video.

5. Stop Playback
You can stop the video playback at any time by pressing the Escape key.

Supported Formats:
The application supports various video formats including:
.mp4
.avi
.mkv
.mov
And more... 

Keyboard Shortcuts

Mark Start: 1
Mark End: 2
Rewind: ← (Left Arrow)
Fast Forward: → (Right Arrow)
Stop: Escape

Requirements

Python 3.6+ (if running from source)
ffmpeg (must be installed separately)
