import os
import time
from playwright.sync_api import sync_playwright
from config.settings import BASE_DIR

COOKIE_DIR = os.path.join(BASE_DIR, "config", "tiktok_session")

def run_tiktok_uploader(video_path, caption):
    print("\n[TikTok] Memulai otomatisasi dengan Google Chrome Engine (Super Stealth)...")
    
    if not os.path.exists(video_path):
        print(f"[Error] File video tidak ditemukan di path: {video_path}")
        return False

    with sync_playwright() as p:
        try:
            # KUNCI: Menambahkan channel="chrome" untuk memicu Google Chrome asli di laptop
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=COOKIE_DIR,
                headless=False,
                channel="chrome", 
                no_viewport=True,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars"
                ],
                ignore_default_args=["--enable-automation"]
            )
        except Exception as e:
            print(f"[Error] Gagi mamicu Google Chrome asli: {e}")
            print("[Info] Pastikan Google Chrome sudah terinstall biasa di laptop lu.")
            return False
        
        page = browser_context.new_page()
        
        # Samarkan sidik jari browser
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['id-ID', 'id', 'en-US', 'en'] });
        """)
        
        print("[TikTok] Membuka halaman login...")
        page.goto("https://www.tiktok.com/login?lang=id-ID")
        
        print("\n" + "="*60)
        print("[PERINGATAN] SILAKAN LOGIN MANUAL DI BROWSER CHROME YANG TERBUKA:")
        print("1. Scan QR atau masuk pakai akun lu.")
        print("2. TUNGGU sampai masuk ke halaman BERANDA / FYP TikTok.")
        print("3. JANGAN TEKAN ENTER di VS Code kalau belum sukses masuk beranda!")
        print("="*60)
        
        input("\n👉 Kalo di browser UDAH MASUK BERANDA, balik ke sini & TEKAN [ENTER]...")
        
        print("\n[TikTok] Mengalihkan ke halaman Creator Center...")
        page.goto("https://www.tiktok.com/creator-center/upload?lang=id-ID")
        
        print("[TikTok] Menyelaraskan dashboard upload... Tunggu halaman dimuat.")
        
        try:
            # Nunggu tombol upload muncul maksimal 20 detik
            page.wait_for_selector("input[type='file']", timeout=20000)
            file_input_locator = page.locator("input[type='file']")
            print("[TikTok] Mantap! Halaman upload terdeteksi.")
        except Exception:
            print("[Error] Gagal mendeteksi input upload.")
            screenshot_path = os.path.join(BASE_DIR, "debug_tiktok_error.png")
            page.screenshot(path=screenshot_path)
            print(f"[Info] Bukti eror baru disimpan di: {screenshot_path}")
            browser_context.close()
            return False
            
        # --- PROSES UPLOAD VIDEO ---
        print(f"[TikTok] Memasukkan file video: {os.path.basename(video_path)}")
        file_input_locator.set_input_files(video_path)
        
        print("[TikTok] Video lagi diupload... Menunggu proses rendering (30 detik)...")
        page.wait_for_timeout(30000) 
        
        # --- PROSES ISI CAPTION ---
        print(f"[TikTok] Mengisi caption: '{caption}'")
        caption_box = page.locator("div[contenteditable='true']").first
        if caption_box.is_visible():
            caption_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            caption_box.fill(caption)
            print("[TikTok] Caption berhasil diisi.")
        
        print("\n" + "="*60)
        print("[SUKSES] Video & Caption berhasil terisi otomatis!")
        print("Silakan cek browser lu untuk memastikan posisinya.")
        print("="*60)
        
        input("\n👉 Kalo lu mau nutup browsermu sekarang, TEKAN [ENTER] DI SINI...")
        
        browser_context.close()
        print("[TikTok] Browser ditutup aman.")
        return True