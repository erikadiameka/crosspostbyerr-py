import os
from uploaders import (
    run_tiktok_uploader,
    run_youtube_uploader,
    run_facebook_uploader,
    run_instagram_uploader
)

def main():
    print("="*60)
    print("         🚀 WELCOME TO CROSSPOST-PY SUPER PANEL 🚀         ")
    print("="*60)

    # 1. Input File Video & Pengecekan
    video_path = input("👉 Masukkan nama/path file video (contoh: testvidio.mp4): ").strip()
    if not os.path.exists(video_path):
        print(f"❌ [Error] File '{video_path}' gak ketemu, bro! Pastiin filenya ada di folder utama.")
        return

    # 2. Input Caption
    caption = input("👉 Masukkan caption/deskripsi video: ").strip()

    # 3. Menu Pilihan Blasting Platform
    print("\n📺 PILIH TARGET PLATFORM BLASTING KONTEN:")
    print("-" * 40)
    print("[1] 🔥 BLAST KE SEMUA API AKTIF (YouTube + Facebook + Instagram)")
    print("[2] 🟥 YouTube Shorts Saja (Official API)")
    print("[3] 🟦 Facebook Page Saja (Official API)")
    print("[4] 🟪 Instagram Reels Saja (API via Cloud Pipeline)")
    print("[5] ⬛ TikTok (Browser Automation - Mode Pemulihan Limit)")
    print("-" * 40)
    
    pilihan = input("👉 Masukkan nomor pilihan lu (1-5): ").strip()

    print("\n" + "="*60)
    print("⚡ MEMULAI ENGINE OTOMATISASI... MOHON TUNGGU ⚡")
    print("="*60)

    # 4. Logika Eksekusi Orkestrasi
    if pilihan == "1":
        print("\n🚀 [BLAST MODE] Menembak 3 Platform Sekaligus...")
        
        print("\n--- [Antrean 1: YouTube] ---")
        run_youtube_uploader(video_path, caption)
        
        print("\n--- [Antrean 2: Facebook] ---")
        run_facebook_uploader(video_path, caption)
        
        print("\n--- [Antrean 3: Instagram] ---")
        run_instagram_uploader(video_path, caption)

    elif pilihan == "2":
        run_youtube_uploader(video_path, caption)
        
    elif pilihan == "3":
        run_facebook_uploader(video_path, caption)
        
    elif pilihan == "4":
        run_instagram_uploader(video_path, caption)
        
    elif pilihan == "5":
        run_tiktok_uploader(video_path, caption)
        
    else:
        print("❌ Pilihan gak ada di menu, bro! Program dibatalkan.")

    print("\n" + "="*60)
    print("🎉 EXECUTION DONE! Semua antrean proses selesai diproses. 🎉")
    print("="*60)

if __name__ == "__main__":
    main()