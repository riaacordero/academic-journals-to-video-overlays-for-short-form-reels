from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import os

video_path = "./data/input_video/video2.mp4"
audio_path = "./output/audio/narration.mp3"
output_video_path = "./output/video/new_video.mp4"

def generate_video(summary):
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path)

    audio_duration = audio_clip.duration
    video_clip = video_clip.subclip(0, audio_duration)

    segments = summary.split(". ")
    segment_duration = audio_duration / len(segments) if segments else audio_duration
    text_clips = []

    # Text overlay for each segment
    for i, segment in enumerate(segments):
        start_time = i * segment_duration
        text_clip = (TextClip(segment.strip(), fontsize=36, color='black', bg_color='white', 
                    size=(video_clip.w * 0.9, None), method='caption', print_cmd=True, font='Helvetica')
                     .set_start(start_time)
                     .set_duration(segment_duration)
                     .set_position(('center', 'center'))
                     .set_opacity(0.8)
                     .crossfadein(0.3)
                     .crossfadeout(0.3))
        
        text_clips.append(text_clip)

    final_video = CompositeVideoClip([video_clip] + text_clips)
    final_video = final_video.set_audio(audio_clip)

    final_video.write_videofile(output_video_path, fps=24)

    print("Video created successfully!")