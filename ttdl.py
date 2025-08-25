import sys, time, os, requests, re, base64
from bs4 import BeautifulSoup

try:
    from pyfiglet import Figlet
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
except ImportError:
    print("Modules Belum Terinstal!!!: bash install_modules.sh")
    sys.exit(1)

# Warna terminal
R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"; C = "\033[96m"; W = "\033[97m"; RESET = "\033[0m"; BOLD = "\033[1m"

# Folder download
DOWNLOAD_DIR = "/sdcard/Download"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ======================
# Fungsi clear layar
# ======================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ======================
# Animasi ketikan intro
# ======================
def type_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def intro():
    clear()
    type_effect(f"{Y}{BOLD}Downloader Tiktok Vidio/Audio No Watermark/Watermark...{RESET}", 0.07)
    time.sleep(0.5)
    type_effect(f"{C}Created By ILHAM A.{RESET}", 0.07)
    time.sleep(2)
    clear()

# ======================
# Fungsi decode URL
# ======================
def extract_url(url: str):
    if not url:
        return None
    match = re.search(r"/(hd|dl|mp3)/([A-Za-z0-9+/=]+)[^\"' ]*", url)
    if match and match.group(2):
        try:
            return base64.b64decode(match.group(2)).decode("utf-8")
        except Exception:
            return url
    return url

# ======================
# Downloader dgn progress bar
# ======================
def download_file(url, filename):
    if not url:
        print(f"{R}✘ URL tidak valid untuk {filename}{RESET}")
        return
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    try:
        r = requests.get(url, stream=True)
        total = int(r.headers.get("content-length", 0))

        with Progress(
            TextColumn("[cyan]⬇️ Mengunduh...[/cyan]"),
            BarColumn(bar_width=30),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(f"[green]{filename}[/green]", total=total)
            with open(filepath, "wb") as f:

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
        print(f"{G}✔ Tersimpan: {filepath}{RESET}")
    except Exception as e:
        print(f"{R}✘ Gagal: {e}{RESET}")

# ======================
# Scraper Musicaldown
# ======================
def musicaldown(tiktok_url: str):
    session = requests.Session()
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10) Chrome/95 Safari/537.36",
        "referer": "https://musicaldown.com/id"
    }

    try:
        res = session.get("https://musicaldown.com/id/download", headers=headers)
        soup1 = BeautifulSoup(res.text, "html.parser")

        url_input = soup1.select_one("input[name][id=link_url]") or soup1.select_one("input[name]")
        if not url_input:
            raise Exception("Input link_url tidak ditemukan (website berubah?)")
        url_name = url_input.get("name")

        hidden_inputs = soup1.select("div.inputbg input[type=hidden]")
        if len(hidden_inputs) < 2:
            raise Exception("Token/verify tidak ditemukan")

        token, verify = hidden_inputs[0], hidden_inputs[1]
        data = {url_name: tiktok_url, token.get("name"): token.get("value"), "verify": verify.get("value")}

        res2 = session.post("https://musicaldown.com/id/download", data=data, headers=headers)
        soup2 = BeautifulSoup(res2.text, "html.parser")

        is_slide = soup2.select("div.card-image")

        if not is_slide:  # video
            res3 = session.post("https://musicaldown.com/id/mp3", headers=headers)
            soup3 = BeautifulSoup(res3.text, "html.parser")
            audio = soup3.select_one('a[data-event="mp3_download_dclick"]') \
                or soup3.select_one('a[data-event="mp3_download_click"]')
            audio = audio["href"] if audio else None

            return {
                "status": True,
                "type": "video",
                "video": extract_url(soup2.select_one('a[data-event="mp4_download_click"]')["href"]) if soup2.select_one('a[data-event="mp4_download_click"]') else None,
                "video_hd": extract_url(soup2.select_one('a[data-event="hd_download_click"]')["href"]) if soup2.select_one('a[data-event="hd_download_click"]') else None,
                "video_wm": extract_url(soup2.select_one('a[data-event="watermark_download_click"]')["href"]) if soup2.select_one('a[data-event="watermark_download_click"]') else None,
                "audio": audio
            }
        else:  # slide
            images = [x.find("img")["src"] for x in is_slide if x.find("img")]
            return {"status": True, "type": "slide", "image": images}
    except Exception as e:
        return {"status": False, "mess": f"{e}"}

# ======================
# Menu + ASCII
# ======================
def main():
    clear()
    f = Figlet(font="future")
    print(f"\n\n\n\n{C}{BOLD}{f.renderText('  TikTok Downloader')}{RESET}")
    print(f"{W}                  Terminal Modern by ILHAM A.{RESET}\n")

    tiktok_url = input(f"{Y}🔗 Masukkan link TikTok:{W} ").strip()
    if not tiktok_url:
        print(f"{R}✘ URL kosong!{RESET}")
        return

    print(f"\n{C}⏳ Sedang memproses...{RESET}\n")
    result = musicaldown(tiktok_url)

    if not result["status"]:
        print(f"{R}✘ Error: {result['mess']}{RESET}")
        return

    clear()  # bersihkan sebelum tampilkan menu pilihan

    if result["type"] == "video":
        print(f"{G}✔ Hasil ditemukan!{RESET}\n")
        print("   1. Video tanpa watermark")
        print("   2. Video HD")
        print("   3. Video dengan watermark")
        print("   4. Audio (MP3)")
        print("   5. Semua")
        print("   0. Keluar")

        choice = input(f"\n👉 Pilih menu: {W}").strip()

        clear()  # clear lagi sebelum download
        if choice == "1":
            download_file(result.get("video"), "tiktok_nowm.mp4")
        elif choice == "2":
            download_file(result.get("video_hd"), "tiktok_hd.mp4")
        elif choice == "3":
            download_file(result.get("video_wm"), "tiktok_wm.mp4")
        elif choice == "4":
            download_file(result.get("audio"), "tiktok_audio.mp3")
        elif choice == "5":
            download_file(result.get("video"), "tiktok_nowm.mp4")
            download_file(result.get("video_hd"), "tiktok_hd.mp4")
            download_file(result.get("video_wm"), "tiktok_wm.mp4")
            download_file(result.get("audio"), "tiktok_audio.mp3")
        else:
            print(f"{Y}👋 Keluar.{RESET}")

    elif result["type"] == "slide":
        print(f"{G}✔ Slide TikTok ditemukan! ({len(result['image'])} gambar){RESET}\n")
        for i, img in enumerate(result["image"], 1):
            print(f"   {i}. {img}")
        choice = input(f"\n👉 Download semua gambar? (y/n): {W}").lower()

        clear()
        if choice == "y":
            for i, img in enumerate(result["image"], 1):
                download_file(img, f"slide_{i}.jpg")
        print(f"\n{G}✔ Selesai! File tersimpan di {DOWNLOAD_DIR}{RESET}")

if __name__ == "__main__":
    intro()  # <<< tampilkan intro sekali di awal
    main()
