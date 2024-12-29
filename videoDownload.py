from moviepy import *

# Load the mp4 file
video = VideoFileClip("./video.mp4")

# Extract audio from video
video.audio.write_audiofile("sample4.mp3")
