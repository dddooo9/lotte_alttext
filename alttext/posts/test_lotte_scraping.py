import csv, requests, re, os
from bs4 import BeautifulSoup


def lotte_scrape():
    # filename = "./alttext/static/lotte_scraping.csv" # shop 스크래핑 데이터 CSV 저장
    # f = open(filename, "w", encoding="utf-8-sig", newline="")
    # writer = csv.writer(f)

    # title = "상세보기 페이지 URL,상품 ID,상세보기 innerHtml URL, 썸네일 URL,브랜드명,상품명,가격".split(",") # CSV 1행
    # writer.writerow(title)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    for i in range(0, 120, 60): # 35 페이지까지 있으므로 최대값 2100
        ni = i / 60
        pni = ni + 1
        # print("="*35)
        # print("상품 리스트", round(pni), "/ 35 페이지 출력됨")
        # print("="*35)

        url = "https://www.lotteon.com/search/render/render.ecn?&u2={}&u3=60&u9=navigateProduct&render=nqapi&platform=pc&collection_id=9&u4=ec10200001".format(i) # 파라미터 u2값에 60 더해지면 다음 페이지
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        # with open("test_lotte_menswear.html", "w", encoding="utf8") as f:
        #     f.write(res.text)
        soup = BeautifulSoup(res.text, "lxml")
        products = soup.find_all("li", attrs={"class": "srchProductItem"})
        for product in products:
            purl = product.div.div.a["href"] # 상세보기 페이지 URL
            id = re.sub('https://www.lotteon.com/p/product/', '', purl)[0:12] # 상품 ID
            if re.sub('https://www.lotteon.com/p/product/', '', purl)[0:2] == "PD": # 상품 ID가 PD로 시작하는 경우 상품 ID
                id = re.sub('https://www.lotteon.com/p/product/', '', purl).replace('?mall_no=1&dp_infw_cd=CASec10200001', '')
            durl = "https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2F"+id[0:2]+"%2F"+id[2:4]+"%2F"+id[4:6]+"%2F"+id[6:8]+"%2F"+id[8:10]+"%2F"+id[10:12]+"%2FDSCRP_"+id # 상세보기 innerHtml URL
            if id[0:2] == "PD": # 상품 ID가 PD로 시작하는 경우 상세보기 innerHtml URL
                dres = requests.get(purl, headers=headers)
                dres.raise_for_status()
                # with open("test_lotte_outer.html", "w", encoding="utf8") as f:
                #     f.write(dres.text)
                dsoup = BeautifulSoup(dres.text, "lxml")
                imgurl = dsoup.find("meta", attrs={"property": "og:image"})["content"]
                id = imgurl[-29:-17]
                durl = "https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2F"+id[0:2]+"%2F"+id[2:4]+"%2F"+id[4:6]+"%2F"+id[6:8]+"%2F"+id[8:10]+"%2F"+id[10:12]+"%2FDSCRP_"+id
            thumb = product.div.div.a.div.img["src"] # 썸네일 URL
            brand = product.find("strong").get_text(strip=True) # 브랜드명
            brand_name = product.find("div", attrs={"class": "srchProductUnitTitle"}).get_text(strip=True)
            except_brand = re.sub(brand, '', brand_name)
            name = except_brand.lstrip('() ') # 상품명
            price = product.find("span", attrs={"class": "srchCurrentPrice"}).get_text(strip=True) # 가격
            # print("상세보기 페이지 URL:", purl, "\n상품 ID:", id, "\n상세보기 innerHtml URL:", durl, "\n썸네일 URL:", thumb, "\n브랜드명:", brand, "\n상품명:", name, "\n가격:", price)
            data = [purl, id, durl, thumb, brand, name, price]
            # print(data)
            # print("-"*150)
            # writer.writerow(data) # shop 스크래핑 데이터 CSV 저장
            
            # ires = requests.get(durl, headers=headers)
            # ires.raise_for_status()
            # # with open("test_lotte_inner.html", "w", encoding="utf8") as f:
            # #     f.write(ires.text)
            # isoup = BeautifulSoup(ires.text, "lxml")
            # innerimgs = isoup.find("span", attrs={"id": "m2root"}).find_all("img")
            # for idx, innerimg in enumerate(innerimgs):
            #     innerimgurl = innerimg["src"]
                
            #     image_res = requests.get(innerimgurl, headers=headers)
            #     if image_res.status_code == requests.codes.ok:
            #         path = "./alttext/static/images/{}".format(id) # 상세이미지 폴더 경로
            #         if not(os.path.isdir(path)):
            #             os.makedirs(os.path.join(path))
            #         with open("./alttext/static/images/{}/{}_{}.jpg".format(id, id, idx+1), "wb") as f: # 상세이미지 JPG 저장
            #             f.write(image_res.content)
            return data

# print(lotte_scrape())