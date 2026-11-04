import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_youtube_data(url):
    ydl_opts = {
        'skip_download': True,
        'ignore_no_formats_error': True,
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id', 'unknown_id')
            title = info.get('title', 'Untitled Video')
            
        transcript_lines = []
        try:
            ytt_api = YouTubeTranscriptApi()
            fetched = ytt_api.fetch(video_id)
            for snippet in fetched:
                start = round(snippet.start, 2)
                end = round(snippet.start + snippet.duration, 2)
                text = snippet.text.replace('\n', ' ')
                transcript_lines.append(f"[{start} - {end}] {text}")
        except Exception:
            try:
                raw_list = YouTubeTranscriptApi.get_transcript(video_id)
                for item in raw_list:
                    start = round(item['start'], 2)
                    end = round(item['start'] + item['duration'], 2)
                    text = item['text'].replace('\n', ' ')
                    transcript_lines.append(f"[{start} - {end}] {text}")
            except Exception as sub_err:
                transcript_lines.append(f"[Transcript unavailable: {sub_err}]")

        raw_transcript = "\n".join(transcript_lines)
        
        ai_pack = f"""[SYSTEM DIRECTIVE: YOUTUBE CLIPPING COMPILER]
ROLE: Analyze the transcript below, select the best viral clips (20-60 seconds each), and reply ONLY with valid JSON.
Every title MUST include context-appropriate #Shorts hashtags directly in the title.

REQUIRED JSON REPLY FORMAT:
{{
  "clips": [
    {{
      "start": 12.5,
      "end": 48.0,
      "title": "Why This Changes Everything #Shorts #Podcast #Viral",
      "description": "Short punchy description of the clip.",
      "tags": ["Shorts", "Podcast", "Viral"]
    }}
  ]
}}

VIDEO URL: {url}
VIDEO TITLE: {title}
TRANSCRIPT:
{raw_transcript}
"""
        return {
            "success": True,
            "video_id": video_id,
            "title": title,
            "ai_pack": ai_pack,
            "is_long_text": len(ai_pack) > 15000
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
