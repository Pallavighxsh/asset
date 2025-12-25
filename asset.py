import os
import requests
import json
from io import BytesIO
from urllib.parse import urlparse
import tkinter as tk
from PIL import Image, ImageTk
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")

CACHE_FILE = "image_cache.json"

# ---------------- Cache Functions ---------------- #

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

# ---------------- Serp API Fetch ---------------- #

def fetch_images(keyword, limit=30, force_refresh=False):
    cache = load_cache()

    # use cached result when possible
    if keyword in cache and not force_refresh:
        print(f"📦 Loaded from cache → {keyword}")
        return cache[keyword]

    print(f"\n🔎 Searching online for: {keyword}")

    search = GoogleSearch({
        "engine": "google",
        "q": keyword,
        "tbm": "isch",
        "ijn": "0",
        "api_key": API_KEY
    })

    results = search.get_dict()
    urls = []

    if "images_results" in results:
        for img in results["images_results"][:limit]:
            url = img.get("original") or img.get("thumbnail")
            if url:
                urls.append(url)

    urls = list(dict.fromkeys(urls))  # dedupe

    cache[keyword] = urls
    save_cache(cache)

    print(f"✔ {len(urls)} images cached")
    return urls


# ---------------- Image Viewer UI ---------------- #

def start_viewer(DATA):
    set_index = 0
    img_index = 0
    current_image = None
    current_url = None

    root = tk.Tk()
    root.title("SerpAPI Image Browser")
    root.geometry("1000x700")

    label = tk.Label(root)
    label.pack(expand=True)

    status = tk.Label(root, text="", font=("Arial", 14))
    status.pack(pady=10)

    def load_image():
        nonlocal current_image, current_url, set_index, img_index
        title, urls, folder = DATA[set_index]

        if img_index >= len(urls):
            next_set()
            return

        current_url = urls[img_index]
        try:
            img = Image.open(BytesIO(requests.get(current_url, timeout=8).content))
        except:
            status.config(text="⛔ Failed to load image. SPACE to skip")
            return

        img.thumbnail((900, 550))
        current_image = img

        tk_img = ImageTk.PhotoImage(img)
        label.config(image=tk_img)
        label.image = tk_img

        status.config(text=f"[{title}] {img_index+1}/{len(urls)}  |  SPACE=Next  ENTER=Save  ESC=Exit")

    def save_image():
        title, urls, folder = DATA[set_index]
        os.makedirs(folder, exist_ok=True)

        parsed = urlparse(current_url)
        name = os.path.basename(parsed.path) or "image.jpg"
        ext = os.path.splitext(name)[1] or ".jpg"

        filename = f"{img_index+1:03d}_{parsed.netloc.replace('.', '_')}{ext}"
        path = os.path.join(folder, filename)

        current_image.save(path)
        status.config(text=f"💾 Saved → {path}")

    def next_img(event=None):
        nonlocal img_index
        img_index += 1
        load_image()

    def next_set():
        nonlocal set_index, img_index
        set_index += 1
        img_index = 0
        if set_index >= len(DATA):
            status.config(text="🎉 All done!")
        else:
            load_image()

    root.bind("<space>", next_img)
    root.bind("<Return>", lambda e: save_image())
    root.bind("<Escape>", lambda e: root.destroy())

    load_image()
    root.mainloop()


# ---------------- MAIN LOGIC ---------------- #

if __name__ == "__main__":
    print("\n=== IMAGE SEARCH TOOL ===")
    kw1 = input("Enter first keyword: ")
    kw2 = input("Enter second keyword: ")

    DATA = [
        (kw1, fetch_images(kw1), kw1.replace(" ", "_")+"_images"),
        (kw2, fetch_images(kw2), kw2.replace(" ", "_")+"_images")
    ]

    start_viewer(DATA)
