# -*- coding: utf-8 -*-
# pip install --upgrade pip --user
import io
import os
import pyocr  # pip install pyocr
import pyocr.builders
from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from PIL import Image, ImageEnhance  # pip install image
import settings

# selenium
# ポートを指定して現在起動中のブラウザのドライバを扱う
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:15134")
driver = webdriver.Chrome(
    service=Service(settings.DRIVER_PATH), 
    options=options
)

# ocr
path_tesseract = "C:/Program Files/Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract
tools = pyocr.get_available_tools()
tool = tools[0]

def auto():
    # 画面操作のためウィンドウサイズを調整
    driver.set_window_size(924, 600)
    x, y, filename = get_coordinates(driver)
    save_filename = screenshot_canvas(driver, x, y, filename)

    img = Image.open(save_filename)
    img.show()

def screenshot_canvas(driver, top_left, bottom_right, filename):
    screenshot = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(screenshot))

  # 座標指定のスクリーンショット
    area = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
    cropped_img = img.crop(area)
    save_filename = filename+"("+str(top_left[0])+", "+str(top_left[1])+", "+str(bottom_right[0])+", "+str(bottom_right[1])+").png"
    cropped_img.save(save_filename)
    
    return save_filename

def get_coordinates(driver):
    # 既存のクリックイベントリスナーを削除
    driver.execute_script("""
    if (window.clickEventListener) {
        document.removeEventListener('click', window.clickEventListener);
    }
    """)

    # マウスのクリックイベントを取得するJavaScriptのコードをWebページに挿入
    driver.execute_script("""
    window.points = [];
    window.clickEventListener = function(event) {
        window.points.push([event.clientX, event.clientY]);
    };
    document.addEventListener('click', window.clickEventListener);
    """)

    filename = input("マウスで2点をクリックした後、画像ファイル名を入力してEnter: ")
    while filename == "":
        print("ファイル名は必ず入力してください。")
        filename = input("画像ファイル名を入力してEnter: ")

    coordinates = driver.execute_script('return window.points')

    return coordinates[0], coordinates[1], filename

if __name__ == '__main__':
    auto()
