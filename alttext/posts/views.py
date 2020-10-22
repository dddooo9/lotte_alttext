import csv, requests, re, os
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.core.paginator import Paginator


def shop(request):
    from .models import Lotte

    all_products = Lotte.objects.all()
    paginator = Paginator(all_products, 12) # 한 페이지에 12개
    page = request.GET.get('page')
    pagenums = paginator.get_page(page)

    # 세션이 만료되지 않은(들어온 적이 있는) 사용자에게는 기존 데이터 보여주고, 세션이 만료된(새로 들어온) 사용자에게는 새로운 데이터 보여주기
    # if request.session.get('previous_user'):
    #     return render(request, 'posts/shop.html', {'products': all_products, 'pagenums': pagenums})
    
    # shop 스크래핑 데이터 CSV 저장
    filename = "./alttext/static/lotte_scraping.csv"
    f = open(filename, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)
    title = "상세보기 페이지 URL,상품 ID,상세보기 innerHtml URL, 썸네일 URL,브랜드명,상품명,가격".split(",")
    writer.writerow(title) # CSV 1행에 컬럼 제목 입력

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    for i in range(0, 180, 60):
        # ri = i / 12 + 1
        # print("="*35)
        # print("롯데온 상품 리스트", round(ri), "/ 3 페이지 출력됨")
        # print("="*35)

        # DB에 스크래핑 데이터 모두 있으면 바로 데이터 보여주기
        # UPDATE: 2020.10.23.
        if len(all_products) > 119:
            return render(request, 'posts/shop.html', {'products': all_products, 'pagenums': pagenums})

        url = "https://www.lotteon.com/search/render/render.ecn?&u2={}&u3=60&u9=navigateProduct&render=nqapi&platform=pc&collection_id=9&u4=ec10200001".format(i) # u2값은 맨 앞 인덱스(0으로 두면 됨), u3값은 맨 뒤 인덱스(롯데온 페이지 나누는 기준 or 총 상품 수, 최대값 100)
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
                imgurl = dsoup.find("meta", attrs={"property": "og:image"})["content"] # 리사이징되지 않은 썸네일 원본 URL
                id = imgurl[-29:-17]
                durl = "http://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2F"+id[0:2]+"%2F"+id[2:4]+"%2F"+id[4:6]+"%2F"+id[6:8]+"%2F"+id[8:10]+"%2F"+id[10:12]+"%2FDSCRP_"+id
            thumb = product.div.div.a.div.img["src"] # 썸네일 URL
            brand = product.find("strong").get_text(strip=True) # 브랜드명
            brand_name = product.find("div", attrs={"class": "srchProductUnitTitle"}).get_text(strip=True) # 브랜드명 + 상품명
            name = re.sub(brand, '', brand_name).lstrip('() ') # 상품명
            price = product.find("span", attrs={"class": "srchCurrentPrice"}).get_text(strip=True) # 가격
            # print("상세보기 페이지 URL:", purl, "\n상품 ID:", id, "\n상세보기 innerHtml URL:", durl, "\n썸네일 URL:", thumb, "\n브랜드명:", brand, "\n상품명:", name, "\n가격:", price)
            data = [purl, id, durl, thumb, brand, name, price] # CSV 저장을 위한 리스트
            # print(data)
            # print("-"*150)
            writer.writerow(data) # CSV 2행부터 shop 스크래핑 데이터 저장

            # 상세이미지 저장
            ires = requests.get(durl, headers=headers, verify=False)
            ires.raise_for_status()
            # with open("test_lotte_inner.html", "w", encoding="utf8") as f:
            #     f.write(ires.text)
            isoup = BeautifulSoup(ires.text, "lxml")
            innerimgs = isoup.find("span", attrs={"id": "m2root"}).find_all("img")
            for idx, innerimg in enumerate(innerimgs):
                innerimgurl = innerimg["src"]
                image_res = requests.get(innerimgurl, headers=headers, verify=False)
                if image_res.status_code == requests.codes.ok:
                    path = "./alttext/static/images/{}".format(id) # 상세이미지 저장 디렉토리
                    if not(os.path.isdir(path)):
                        os.makedirs(os.path.join(path))
                    with open("./alttext/static/images/{}/{}_{}.jpg".format(id, id, idx+1), "wb") as f: # 상세이미지 JPG 저장
                        f.write(image_res.content)

            p_id = id
            p_detail_url = purl
            p_detail_inner_url = durl
            p_thumb_url = thumb
            p_brand = brand
            p_name = name
            p_price = price
            Lotte.objects.create(p_id=p_id, p_detail_url=p_detail_url, p_detail_inner_url=p_detail_inner_url, p_thumb_url=p_thumb_url, p_brand=p_brand, p_name=p_name, p_price=p_price)
    
    # request.session['previous_user'] = True # 이제 더 이상 세션이 만료된(새로 들어온) 사용자가 아님
    # request.session.set_expiry(43200) # 세션 12시간 유지
    return render(request, 'posts/shop.html', {'products': all_products, 'pagenums': pagenums})


#상품 상세보기 페이지
