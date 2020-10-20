'''
.py 파일명과 import 모듈명 일치 시 'most likely due to a circular import' 에러 발생
따라서 .py 파일명에 'lotte_' prefix 붙임
'''

import csv, requests, re, os
from bs4 import BeautifulSoup

filename = "./alttext/lotte_scraping.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "상세URL,상품ID,상세innerURL,썸네일URL,브랜드명,상품명,가격".split(",")
writer.writerow(title)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

for i in range(0, 60, 60): # 남성의류 카테고리에 35 페이지까지 있으므로 최대값은 2100
    ni = i / 60
    pni = ni + 1
    print("="*35)
    print("상품 리스트", round(pni), "/ 35 페이지 출력됨")
    print("="*35)

    url = "https://www.lotteon.com/search/render/render.ecn?&u2={}&u3=60&u9=navigateProduct&render=nqapi&platform=pc&collection_id=9&u4=ec10200001".format(i) # 파라미터 u2값에 60이 더해질 때마다 다음 페이지 반환
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    products = soup.find_all("li", attrs={"class": "srchProductItem"})
    for product in products:
        purl = product.div.div.a["href"] # 상품 상세보기 페이지 URL
        id = re.sub('https://www.lotteon.com/p/product/', '', purl)[0:12] # 상품 ID
        if re.sub('https://www.lotteon.com/p/product/', '', purl)[0:2] == "PD": # 상품 ID가 PD로 시작하는 경우 대응
            id = re.sub('https://www.lotteon.com/p/product/', '', purl).replace('?mall_no=1&dp_infw_cd=CASec10200001', '')
        durl = "https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2F"+id[0:2]+"%2F"+id[2:4]+"%2F"+id[4:6]+"%2F"+id[6:8]+"%2F"+id[8:10]+"%2F"+id[10:12]+"%2FDSCRP_"+id # 상품 상세보기 innerHtml URL
        if id[0:2] == "PD": # 상품 ID가 PD로 시작하는 경우 진짜 ID 찾기
            dres = requests.get(purl, headers=headers)
            dres.raise_for_status()
            dsoup = BeautifulSoup(dres.text, "lxml")
            imgurl = dsoup.find("meta", attrs={"property": "og:image"})["content"]
            id = imgurl[-29:-17]
            durl = "https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2F"+id[0:2]+"%2F"+id[2:4]+"%2F"+id[4:6]+"%2F"+id[6:8]+"%2F"+id[8:10]+"%2F"+id[10:12]+"%2FDSCRP_"+id
            # with open("test_lotte_inner.html", "w", encoding="utf8") as f:
            #     f.write(dres.text)
        thumb = product.div.div.a.div.img["src"] # 상품 썸네일 이미지 URL
        brand = product.find("strong").get_text(strip=True) # 상품 브랜드명 (strip=True로 공백 제거)
        brand_name = product.find("div", attrs={"class": "srchProductUnitTitle"}).get_text(strip=True)
        except_brand = re.sub(brand, '', brand_name)
        name = except_brand.lstrip('() ') # 상품명 (원본 소스에서는 상품명 엘레먼트 자체에 브랜드명이 포함돼있어, 브랜드명 제거)
        price = product.find("span", attrs={"class": "srchCurrentPrice"}).get_text(strip=True) # 상품 가격
        # print("상세URL:", purl, "\n상품ID:", id, "\n상세innerURL:", durl, "\n썸네일URL:", thumb, "\n브랜드명:", brand, "\n상품명:", name, "\n가격:", price)
        list = [purl, id, durl, thumb, brand, name, price]
        # print(list)
        # print("-"*150)
        writer.writerow(list)
        
        ires = requests.get(durl, headers=headers)
        ires.raise_for_status()
        isoup = BeautifulSoup(ires.text, "lxml")
        # with open("test_lotte_inner.html", "w", encoding="utf8") as f:
        #     f.write(ires.text)
        innerimgs = isoup.find("span", attrs={"id": "m2root"}).find_all("img")
        for idx, innerimg in enumerate(innerimgs):
            innerimgurl = innerimg["src"]
            # print(innerimgurl)
            # list = [purl, id, durl, thumb, brand, name, price, innerimgurl]
            # print(list)
            image_res = requests.get(innerimgurl)
            # image_res.raise_for_status()
            if image_res.status_code == requests.codes.ok:
                path = "./alttext/innerimgs"
                if not os.path.isdir(path):
                    os.mkdir(path)
                with open("./alttext/innerimgs/{}_{}.jpg".format(id, idx+1), "wb") as f:
                    f.write(image_res.content)
            

# 페이지 소스 참고용 HTML 생성    
# with open("test_lotte_outer.html", "w", encoding="utf8") as f:
#     f.write(res.text)

''' 삽질했던 것들.........
# 롯데온 특정 페이지 URL
url = "https://www.lotteon.com/search/render/render.ecn?render=nqapi&platform=pc&collection_id=9&u9=navigate&u8=EC10200000"

# 스크래핑 차단 시 우회하기 위한 User-Agent
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

# 스크래핑 봇이 아니라 실제 사람인 척 접근
res = requests.get(url, headers=headers)

# res.status_code가 200이면 진행, 아니면 종료
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
scripts = soup.find_all("script", attrs={"type": "application/javascript"})
inner = scripts[2]
# print(inner)
p = re.compile("https://contents.lotteon.com/itemimage/\S+360x360")
ms = p.findall(str(inner))

print(ms)

# soup.엘레먼트
# >>> soup 객체에서 맨 처음 발견되는 해당 엘레먼트

# soup.엘레먼트.attrs
# >>> soup 객체에서 맨 처음 발견되는 해당 엘레먼트의 어트리뷰트

# soup.엘레먼트["어트리뷰트"]
# >>> soup 객체에서 맨 처음 발견되는 해당 엘레먼트의 어트리뷰트 밸류 (해당 페이지의 소스를 잘 알고 있을 때?)

# soup.find("엘레먼트", attrs={"어트리뷰트":"밸류"})
# >>> soup 객체에서 해당 어트리뷰트 밸류를 가진 맨 처음 발견되는 엘레멘트 (해당 페이지의 소스를 잘 모를 때?)

# soup.find("엘레멘트", attrs={"어트리뷰트":"밸류"})["다른 어트리뷰트"]
# >>> (요렇게도 쓸 수 있겠지?)

# next_sibling          : 형제 관계에 있는 다음 값 (공백 포함)
# find_next_sibling     : 형제 관계에 있는 다음 값 (공백 미포함)
# previous_sibling      : 형제 관계에 있는 이전 값 (공백 포함)
# find_previous_sibling : 형제 관계에 있는 이전 값 (공백 미포함)
# parent                : 부모 관계에 있는 값
# find_all              : 맨 처음 발견되는 것뿐만 아니라 해당하는 전부 (list로 반환하므로 다음 코드에 인덱스 값 필요)

# status_code가 200이면 정상, 403이면 접근권한 없다는 뜻
# status_code가 403이면 해당 서버에서 스크래핑 봇을 차단한 것이므로 사람인 척 접근하기 위해 User-Agent 처리 필요
# 'status_code가 200' == requests.codes.ok

# 스크래핑한 것을 새 파일로 생성
with open("lotte_list_inner.html", "w", encoding="utf8") as f:
    f.write(str(inner))
'''