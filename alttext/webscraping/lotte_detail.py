import requests, re
from bs4 import BeautifulSoup
from lotte_scraping import durl

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

# url = "https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2FLO%2F13%2F06%2F57%2F45%2F55%2FDSCRP_LO1306574555"
url = durl
res = requests.get(url, headers=headers)
res.raise_for_status()

# soup = BeautifulSoup(res.text, "lxml")
# imgs = soup.find_all("span", attrs={"id": "m2root"})
# for img in imgs:
#     jpgs = img.find_all()

with open("test_lotte_detail.html", "w", encoding="utf8") as f:
    f.write(res.text)

# print(url)