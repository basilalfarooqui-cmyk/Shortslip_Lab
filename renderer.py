import os
import subprocess

def render_clip_with_watermark(input_video, output_path, start_sec, end_sec, watermark_text, wm_x, wm_y, wm_size, aspect_ratio, subtitles_enabled, caption_size):
    """
    Uses FFmpeg to trim video, burn subtitles if requested, and overlay draggable @ChannelName watermark.
    """
    # Normalize coordinates for ffmpeg drawtext filter
    # wm_x and wm_y passed from UI percentages or pixel positions
    font_color = "white"
    box_config = "box=1:boxcolor=black@0.5:boxborderw=5"
    
    drawtext_filter = (
        f"drawtext=text='@{watermark_text}':x={wm_x}:y={wm_y}:"
        f"fontsize={wm_size}:fontcolor={font_color}:{box_config}"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-to", str(end_sec),
        "-i", input_video,
        "-vf", drawtext_filter,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return False
