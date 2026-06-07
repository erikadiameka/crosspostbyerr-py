import os
import requests
from config.settings import META_ACCESS_TOKEN, FACEBOOK_PAGE_ID

def run_facebook_uploader(video_path, caption):
    print("\n[Facebook] Memulai proses upload via Meta Graph API...")
    
    if not os.path.exists(video_path):
        print(f"[Error] File video tidak ditemukan di path: {video_path}")
        return False
        
    if not META_ACCESS_TOKEN or not FACEBOOK_PAGE_ID:
        print("[Error] META_ACCESS_TOKEN atau FACEBOOK_PAGE_ID belum diisi di file .env!")
        return False

    # Endpoint Graph API untuk upload video ke Page
    url = f"https://graph.facebook.com/v20.0/{FACEBOOK_PAGE_ID}/videos"
    
    payload = {
        'description': caption,
        'access_token': META_ACCESS_TOKEN
    }
    
    try:
        print(f"[Facebook] Mengunggah {os.path.basename(video_path)} langsung ke server Meta...")
        
        # Buka file video dalam mode binary dan kirim via multipart/form-data
        with open(video_path, 'rb') as video_file:
            files = {
                'source': video_file
            }
            response = requests.post(url, data=payload, files=files)
            
        result = response.json()
        
        if response.status_code == 200 and "id" in result:
            print(f"[SUKSES] Video berhasil terbit di Facebook Page! Video ID: {result['id']}")
            return True
        else:
            error_msg = result.get('error', {}).get('message', 'Eror tidak diketahui')
            print(f"[Error] Gagal upload ke Facebook: {error_msg}")
            return False
            
    except Exception as e:
        print(f"[Error] Terjadi kendala koneksi saat menghubungi API Facebook: {e}")
        return False