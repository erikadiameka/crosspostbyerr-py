import os
from uploaders.tiktok import run_tiktok_uploader

def main():
    print("="*50)
    print("      CROSSPOST-PY TERMINAL CONTROLLER      ")
    print("="*50)
    
    # Masukkan data dummy buat ngetes jalan atau enggak script-nya
    # TIPS: Taruh satu file video mp4 pendek di folder project kamu buat testing
    video_file = input("Masukkan nama file video untuk test (contoh: video.mp4): ")
    caption_text = "Mencoba project open source CrossPost-Py! #python #developer"
    
    # Ambil full path dari file video tersebut
    video_full_path = os.path.abspath(video_file)
    
    print(f"\n[Sistem] Menyiapkan pengunggahan...")
    
    # Jalankan modul TikTok
    sukses = run_tiktok_uploader(video_full_path, caption_text)
    
    if sukses:
        print("\n[Sistem] Eksekusi automation tahap awal sukses!")
    else:
        print("\n[Sistem] Eksekusi gagal. Periksa error di atas.")

if __name__ == "__main__":
    main()
    