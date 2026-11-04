import yt_dlp
import os

def parse_instagram_input(url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
    }
    
    reels_list = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            for entry in info['entries']:
                reels_list.append({
                    'id': entry.get('id'),
                    'title': entry.get('title', 'Instagram Reel'),
                    'url': entry.get('url')
                })
        else:
            reels_list.append({
                'id': info.get('id'),
                'title': info.get('title', 'Instagram Reel'),
                'url': url
            })
            
    return reels_list

def generate_reel_ai_pack(reels):
    reels_summary = "\n".join([f"- ID: {r['id']} | Title: {r['title']}" for r in reels])
    ai_pack = f"""[SYSTEM DIRECTIVE: REELS TO SHORTS METADATA COMPILER]
ROLE: Generate fresh, punchy titles with context-appropriate #Shorts hashtags for downloaded Instagram reels.
INPUT REELS:
{reels_summary}
"""
    return ai_pack
