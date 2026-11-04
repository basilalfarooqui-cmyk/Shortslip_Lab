import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_fresh_youtube_service():
    """
    No local token storage: Forces fresh browser OAuth login every time called.
    """
    if not os.path.exists(CLIENT_SECRET_FILE):
        raise FileNotFoundError("Missing client_secret.json in project root directory.")
        
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    # Runs local server to capture fresh auth code without storing token.pickle
    creds = flow.run_local_server(port=0, prompt='consent')
    return build("youtube", "v3", credentials=creds)

def upload_short_to_youtube(video_path, title, description, tags, publish_iso):
    youtube = get_fresh_youtube_service()
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22" # People & Blogs
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_iso,
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        
    return response.get("id")
