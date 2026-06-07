import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from config.settings import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET

# Scope wajib untuk upload video ke YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service():
    # Membuat konfigurasi client dari setting .env
    client_config = {
        "web": {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    # Jalankan login browser local untuk dapet izin akses (OAuth2)
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def run_youtube_uploader(video_path, caption):
    print("\n[YouTube] Memulai proses upload via YouTube Data API v3...")
    
    if not os.path.exists(video_path):
        print(f"[Error] File video tidak ditemukan di path: {video_path}")
        return False
        
    if not YOUTUBE_CLIENT_ID or not YOUTUBE_CLIENT_SECRET:
        print("[Error] YOUTUBE_CLIENT_ID atau YOUTUBE_CLIENT_SECRET belum dikonfigurasi di .env!")
        return False

    try:
        youtube = get_youtube_service()
        
        # Konfigurasi metadata video
        body = {
            'snippet': {
                'title': caption[:100], # Batasan judul YT maks 100 karakter
                'description': caption,
                'tags': ['python', 'automation', 'crosspost'],
                'categoryId': '28' # Kategori Tech/Science
            },
            'status': {
                'privacyStatus': 'public', # Langsung publik atau ganti 'private'/'unlisted'
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Siapkan file untuk di-upload secara berkala (chunked)
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/*')
        
        print(f"[YouTube] Mengunggah {os.path.basename(video_path)}...")
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        
        response = request.execute()
        
        if "id" in response:
            print(f"[SUKSES] Video berhasil mendarat di YouTube! Video ID: {response['id']}")
            print(f"Link: https://youtu.be/{response['id']}")
            return True
        else:
            print("[Error] Respons YouTube tidak menyertakan Video ID.")
            return False
            
    except Exception as e:
        print(f"[Error] Terjadi kegagalan saat upload ke YouTube: {e}")
        return False