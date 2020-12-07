"""
批量下载百度图片
"""
import re
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome()
# driver.maximize_window()
# 设置chrome浏览器无界面模式
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
# 无界面模式下默认不是全屏，所以需要设置一下分辨率
driver.set_window_size(1920, 1080)
driver.get('')
time.sleep(10)
for j in range(8):
    driver.execute_script("var action=document.documentElement.scrollTop=10000")
time.sleep(1)
for i in range(100):
    url = driver.find_element_by_xpath('//*[@id="imgid"]/div[9]/ul/li[' + str(i + 5) + ']/div/a/img').get_attribute(
        'src')
    print(url)
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        with open('D:\\picccc\\' + str(i + 79) + '.jpg', 'wb') as fp:
            fp.write(get_img)
        print("图片下载完成")
    except:
        print("访问空")
    continue
