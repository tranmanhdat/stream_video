# stream_video

#TO RUN:
1. install ffmpeg : `sudo apt install ffmpeg`
2. install requirement : `pip install -r requirements.txt`
3. run code:
- `sudo ffserver -f server.conf`
- python main.py --rtsp_link <rtsp link> | ffmpeg -f rawvideo -pixel_format
 bgr24
 -video_size
 1280x720 -i
 \- http://localhost:8090/fac1.ffm   
 - python main.py --rtsp_link <rtsp link> | ffmpeg -f rawvideo -pixel_format
 bgr24
 -video_size
 1280x720 -i
 \- http://localhost:8090/fac2.ffm  
 - python main.py --rtsp_link <rtsp link> | ffmpeg -f rawvideo -pixel_format
 bgr24
 -video_size
 1280x720 -i
 \- http://localhost:8090/fac3.ffm  
 - python main.py --rtsp_link <rtsp link> | ffmpeg -f rawvideo -pixel_format
 bgr24
 -video_size
 1280x720 -i
 \- http://localhost:8090/fac4.ffm  
Then go to browser: [http://localhost:8090/facstream.mjpeg](http://localhost
:8090/facstream1.mjpeg) or http://<ip>:8090/facstream1.mjpeg (or facstream2
.mjpeg, facstream3.mjpeg, facstream4.mjpeg)