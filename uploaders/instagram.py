import os
import time
import requests
from config.settings import META_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID

def upload_to_temporary_host(local_path):
    """
    Mengunggah file video lokal ke temporary host untuk mendapatkan URL publik.
    Instagram Graph API wajib menggunakan URL publik (tidak bisa file lokal langsung).
    """
    print("[Instagram] Mengompres & menitipkan video ke temporary public server...")
    url = "https://tmpfiles.org/api/v1/upload"
    
    try:
        with open(local_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            
        if response.status_code == 201:
            res_data = response.json()
            # Ubah URL biasa menjadi URL Direct Download (wajib bagi Instagram)
            # Contoh: https://tmpfiles.org/123/video.mp4 -> https://tmpfiles.org/dl/123/video.mp4
            file_url = res_data['data']['url'].replace("https://tmpfiles.org/", "https://tmpfiles.org/dl/")
            print(f"[Instagram] URL Publik sukses dibuat: {file_url}")
            return file_url
        else:
            print(f"[Error] Gagal membuat URL publik. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"[Error] Gagal saat proses upload sementara: {e}")
        return None

def run_instagram_uploader(video_path, caption):
    print("\n[Instagram] Memulai proses upload Reels via Meta Graph API...")
    
    if not os.path.exists(video_path):
        print(f"[Error] File video tidak ditemukan di path: {video_path}")
        return False
        
    if not META_ACCESS_TOKEN or not INSTAGRAM_BUSINESS_ACCOUNT_ID:
        print("[Error] META_ACCESS_TOKEN atau INSTAGRAM_BUSINESS_ACCOUNT_ID belum diisi di .env!")
        return False

    # 1. Dapatkan URL publik dari video lokal
    public_video_url = upload_to_temporary_host(video_path)
    if not public_video_url:
        print("[Error] Proses dihentikan karena gagal mendapatkan URL video publik.")
        return False

    # 2. Buat Media Container untuk Instagram Reels
    print("[Instagram] Membuat container media Reels...")
    container_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    
    payload = {
        'media_type': 'REELS',
        'video_url': public_video_url,
        'caption': caption,
        'access_token': META_ACCESS_TOKEN
    }
    
    try:
        response = requests.post(container_url, data=payload)
        res_data = response.json()
        
        if "id" not in res_data:
            print(f"[Error] Gagal membuat container: {res_data.get('error', {}).get('message', 'Unknown Error')}")
            return False
            
        container_id = res_data['id']
        print(f"[Instagram] Container berhasil dibuat. ID: {container_id}")
        
        # 3. Proses Polling (Menunggu server Instagram selesai mendownload & memproses video)
        print("[Instagram] Menunggu server Instagram melakukan pengecekan video (Polling)...")
        status_url = f"https://graph.facebook.com/v20.0/{container_id}"
        status_params = {
            'fields': 'status_code,failure_reason',
            'access_token': META_ACCESS_TOKEN
        }
        
        # Lakukan looping ngecek status per 5 detik (maksimal 2 menit)
        for attempt in range(24):
            time.sleep(5)
            status_res = requests.get(status_url, params=status_params).json()
            status_code = status_res.get('status_code')
            
            print(f" -> Status Reels saat ini: {status_code}")
            
            if status_code == "FINISHED":
                print("[Instagram] Video dinyatakan VALID dan siap rilis!")
                break
            elif status_code == "ERROR":
                print(f"[Error] Instagram menolak video. Alasan: {status_res.get('failure_reason')}")
                return False
        else:
            print("[Error] Timeout! Server Instagram terlalu lama memproses video lu.")
            return False

        # 4. Publish Reels ke Feed Akun Instagram Business
        print("[Instagram] Menayangkan Reels secara resmi ke profil lu...")
        publish_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
        publish_payload = {
            'creation_id': container_id,
            'access_token': META_ACCESS_TOKEN
        }
        
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        if "id" in publish_res:
            print(f"[SUKSES] Reels lu berhasil mengudara di Instagram! ID Post: {publish_res['id']}")
            return True
        else:
            print(f"[Error] Gagal mempublikasikan Reels: {publish_res.get('error', {}).get('message')}")
            return False
            
    except Exception as e:
        print(f"[Error] Terjadi kendala saat eksekusi API Instagram: {e}")
        return False