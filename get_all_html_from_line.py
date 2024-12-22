from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# ตั้งค่า WebDriver
service = Service("C:/ChromeWebDriver/chromedriver.exe")  # เปลี่ยน path ให้ตรงกับเครื่องของคุณ
driver = webdriver.Chrome(service=service)

# URL ของหน้า LINE VOOM
url = "https://linevoom.line.me/user/_dVGZeasMp7vr0djZxioT2R00ZSTeY2iQFLoZ278"
driver.get(url)

time.sleep(5)  # รอให้หน้าโหลด

# ดึง HTML ทั้งหน้า
html_content = driver.page_source

# บันทึก HTML ลงไฟล์
with open("linevoom_page.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("ดึง HTML ของหน้าเว็บสำเร็จและบันทึกลงไฟล์ linevoom_page.html")

# ปิด WebDriver
driver.quit()
