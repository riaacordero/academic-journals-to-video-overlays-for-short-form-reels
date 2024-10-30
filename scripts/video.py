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

    segments = rewritten_summary.split(". ")
    segment_duration = audio_duration / len(segments)
    text_clips = []

    # Text overlay for each segment
    for i, segment in enumerate(segments):
        start_time = i * segment_duration

        text_clip = (TextClip(segment, fontsize=24, color='white', bg_color='black', size=video_clip.size)
                     .set_start(start_time)
                     .set_duration(segment_duration)
                     .set_position('bottom')
                     .set_opacity(0.7))
        
        text_clips.append(text_clip)

    final_video = CompositeVideoClip([video_clip] + text_clips)
    final_video = final_video.set_audio(audio_clip)

    final_video.write_videofile(output_video_path, fps=24)

    print("Video created successfully!")