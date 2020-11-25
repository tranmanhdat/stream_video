1. sudo apt-get install portaudio19-dev python-pyaudio
2. pip install PyAudio
3. sudo python3 get_audio_from_mic.py 
4. run server ffserver: `sudo ffserver -f server.conf`
5. python main.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size vga -i
 \- http://localhost:8090/fac.ffm
 5. http://localhost:8090/facstream.mjpeg