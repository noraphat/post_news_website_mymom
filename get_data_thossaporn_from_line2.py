from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, requests

#Chrome Driver Download
#https://googlechromelabs.github.io/chrome-for-testing/

# --- ตั้งค่า WebDriver ------------------------------------------------------
options = Options()
options.add_argument("--log-level=3")
# service = Service(r"C:/ChromeWebDriver/chromedriver.exe")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://linevoom.line.me/user/_dVGZeasMp7vr0djZxioT2R00ZSTeY2iQFLoZ278"
driver.get(url)

# ---------- ฟังก์ชันช่วยเลื่อนหน้าจอ --------------------------------------
def scroll_until_posts_loaded(target):
    """
    เลื่อนหน้าจอลงทีละ step จนกว่าจะพบโพสต์อย่างน้อย 'target' รายการ
    หรือเลื่อนไปจนสุดเพจ (กันกรณีมีโพสต์น้อยกว่าที่ขอ)
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    retry = 0                      # กัน loop ไม่รู้จบถ้าเจอทางตัน
    MAX_RETRY = 5

    while True:
        posts = driver.find_elements(By.CSS_SELECTOR, "article.vw_feed_post")
        if len(posts) >= target:
            break

        # เลื่อนลงล่างสุดของเพจ
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)              # รอคอนเทนต์ใหม่โหลด

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            retry += 1
            if retry >= MAX_RETRY:  # เพจไม่ขยับแล้ว — คงไม่มีโพสต์เพิ่ม
                break
        else:
            retry = 0
            last_height = new_height

# ---------- ฟังก์ชันเก็บโพสต์ -----------------------------------------------
def scrape_posts(num_posts=70):
    scroll_until_posts_loaded(num_posts)

    posts = driver.find_elements(By.CSS_SELECTOR, "article.vw_feed_post")
    data = []

    for idx, post in enumerate(posts[:num_posts]):   # ตัดให้ตรงตามจำนวนขอ
        try:
            content = post.find_element(By.CSS_SELECTOR, "div.text_viewer").text

            images = post.find_elements(By.CSS_SELECTOR, "img.media_image")
            image_urls = [img.get_attribute("src") for img in images]

            # สร้างโฟลเดอร์ดาวน์โหลดรูป
            image_folder = f"post_{idx + 1}_images"
            os.makedirs(image_folder, exist_ok=True)
            for img_idx, img_url in enumerate(image_urls):
                img_data = requests.get(img_url).content
                with open(f"{image_folder}/image_{img_idx + 1}.jpg", "wb") as img_file:
                    img_file.write(img_data)

            data.append({
                "post_id": idx + 1,
                "content": content,
                "images": image_urls
            })

            print(f"✅ โพสต์ที่ {idx+1} เก็บข้อมูลเรียบร้อย")

        except Exception as e:
            print(f"⚠️  เกิดข้อผิดพลาดในโพสต์ที่ {idx+1}: {e}")

    # บันทึกลงไฟล์ JSON
    with open("posts_data.json", "w", encoding="utf-8") as jf:
        json.dump(data, jf, ensure_ascii=False, indent=4)
    print(f"\nดึงข้อมูล {len(data)} โพสต์เสร็จแล้ว บันทึกเป็น posts_data.json")

# ---------------- เรียกใช้งาน ------------------------------------------------
scrape_posts(num_posts=31)     # อยากได้กี่โพสต์ก็เปลี่ยนตรงนี้

driver.quit()
