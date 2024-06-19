from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url="https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=020&ta=14&jspIdFlg=patternShikugun&sc=14206&kb=1&kt=9999999&km=1&tb=0&tt=9999999&hb=0&ht=9999999&ekTjCd=&ekTjNm=&tj=0&kw=1"
bukken_detail_list=[]

driver.get(url)
time.sleep(3)

bukken_tags=driver.find_elements(By.CSS_SELECTOR,"h2>a")

bukken_href_list=[]

for bukken_tag in bukken_tags:
    bukken_href=bukken_tag.get_attribute("href")
    bukken_href_list.append(bukken_href)

print(len(bukken_href_list))

for bukken in bukken_href_list:
    driver.get(bukken)
    time.sleep(3)

    try:
        bukken_name=driver.find_element(By.XPATH,"//div[contains(text(), '物件名')]/../following-sibling::td[1]").text
    except:
        bukken_name=driver.find_element(By.CSS_SELECTOR,"div>div>h1").text
    finally:
        bukken_name=bukken_name.replace("\u3000"," ")
    try:
        bukken_price=driver.find_element(By.XPATH,"//tr/td/p[contains(text(), '0万円')]").text
    except:
        bukken_price="未定"
    shikichi=driver.find_element(By.XPATH,"//div[contains(text(), '土地面積')]/../following-sibling::td[1]").text
    try:
        yukamenseki=driver.find_element(By.XPATH,"//div[contains(text(), '建物面積')]/../following-sibling::td[1]").text
    except:
        yukamenseki="土地のみ"
    address=driver.find_element(By.XPATH,"//div[contains(text(), '所在地')]/../following-sibling::td[1]").text
    access=driver.find_element(By.XPATH,"//div[contains(text(), '交通')]/../following-sibling::td[1]").text
    access=access.replace('[ 乗り換え案内 ]','')
    access=access.replace('\n','')
    try:
        year=driver.find_element(By.XPATH,"//div[contains(text(), '築年月')]/../following-sibling::td[1]").text
    except:
        year="土地のみ"
    toiawase=driver.find_element(By.XPATH,"//th[contains(text(), 'お問い合せ先')]/following-sibling::td/p").text
    toiawase=toiawase.replace('\u3000',' ')

    bukken_detail_dict={"物件名":bukken_name,"価格":bukken_price,"土地面積":shikichi,"建物面積":yukamenseki,"住所":address,"アクセス":access,"築年数":year,"お問い合わせ先":toiawase}
    print(bukken_detail_dict)

    bukken_detail_list.append(bukken_detail_dict)

df=pd.DataFrame(bukken_detail_list)
df.to_excel("suumo_deta.xlsx")

driver.quit()