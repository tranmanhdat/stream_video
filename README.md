# stream_video

#TO RUN:
1. install ffmpeg : `sudo apt install ffmpeg`
2. install requirement : `pip install -r requirements.txt`
3. run code:
- `sudo ffserver -f server.conf`
- python main.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size vga -i
 \- http://localhost:8090/fac.ffm   
Then go to browser: [localhost](http://localhost:8090/facstream.mjpeg)