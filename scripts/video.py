from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

# MODIFY YOUR FILE PATH IF NEEDED:
video_path = "./data/input_video/video2.mp4"
audio_path = "./output/audio/narration.mp3"
output_video_path = "./output/video/new_video.mp4"

# Load the audio and image
audio_clip = AudioFileClip(audio_path)
video_clip = VideoFileClip(video_path)

# Trim the video to match the audio length
audio_duration = audio_clip.duration
video_clip = video_clip.subclip(0, audio_duration)

video = video_clip.set_audio(audio_clip)

video.write_videofile(output_video_path, fps=24)

print("Video created successfully!")
