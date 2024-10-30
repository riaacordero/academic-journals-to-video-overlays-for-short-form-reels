from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

video_path = "./data/input_video/video2.mp4"
audio_path = "./output/audio/narration.mp3"
output_video_path = "./output/video/new_video.mp4"

def generate_video(rewritten_summary):
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)

    audio_duration = audio_clip.duration
    video_clip = video_clip.subclip(0, audio_duration)

    # Create a text overlay using the rewritten summary
    text_clip = TextClip(rewritten_summary, fontsize=24, color='white', bg_color='black', size=video_clip.size)
    text_clip = text_clip.set_duration(audio_duration).set_position('bottom').set_opacity(0.7)

    # Combine the video and text overlay
    final_video = CompositeVideoClip([video_clip, text_clip])
    final_video = final_video.set_audio(audio_clip)

    final_video.write_videofile(output_video_path, fps=24)

    print("Video created successfully!")
