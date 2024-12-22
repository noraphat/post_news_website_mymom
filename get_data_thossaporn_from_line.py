from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import json
import os
import requests

# ตั้งค่า WebDriver
service = Service("C:/ChromeWebDriver/chromedriver.exe")  # เปลี่ยน path ให้ตรงกับเครื่องคุณ
driver = webdriver.Chrome(service=service)

# URL ของหน้า LINE VOOM
url = "https://linevoom.line.me/user/_dVGZeasMp7vr0djZxioT2R00ZSTeY2iQFLoZ278"
driver.get(url)

time.sleep(5)  # รอให้หน้าโหลด

# ฟังก์ชันดึงข้อมูลโพสต์
def scrape_posts():
    posts = driver.find_elements(By.CSS_SELECTOR, "article.generalPostLayout_feed_post__9CnYc")
    data = []

    for idx, post in enumerate(posts):
        try:
            # ดึงข้อความในโพสต์
            content = post.find_element(By.CSS_SELECTOR, "div.text_viewer").text
            print(f"โพสต์ที่ {idx + 1}: {content}")

            # ดึงรูปภาพในโพสต์
            images = post.find_elements(By.CSS_SELECTOR, "img.media_image")
            image_urls = [img.get_attribute("src") for img in images]
            print(f"รูปภาพในโพสต์ที่ {idx + 1}: {image_urls}")

            # ดาวน์โหลดรูปภาพ
            image_folder = f"post_{idx + 1}_images"
            os.makedirs(image_folder, exist_ok=True)
            for img_idx, img_url in enumerate(image_urls):
                img_data = requests.get(img_url).content
                with open(f"{image_folder}/image_{img_idx + 1}.jpg", "wb") as img_file:
                    img_file.write(img_data)

            # เก็บข้อมูลในรูปแบบ JSON
            data.append({"post_id": idx + 1, "content": content, "images": image_urls})

        except Exception as e:
            print(f"เกิดข้อผิดพลาดในโพสต์ที่ {idx + 1}: {e}")

    # บันทึกข้อมูลลงไฟล์ JSON
    with open("posts_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("ดึงข้อมูลสำเร็จและบันทึกลงไฟล์ posts_data.json")

# เรียกใช้งานฟังก์ชัน
scrape_posts()

# ปิด WebDriver
driver.quit()
