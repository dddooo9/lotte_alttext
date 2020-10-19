'''
.py 파일명과 import 모듈명 일치 시 'most likely due to a circular import' 에러 발생
따라서 .py 파일명에 'lotte_' prefix 붙임
'''

import requests, re
from bs4 import BeautifulSoup

''' 보이는 페이지 그대로 url 변수에 넣은 것
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

# soup.find("엘레멘트", attrs={"어트리뷰트":"밸류"})["어트리뷰트"]
# >>> (요렇게도 쓸 수 있겠지?)

# next_sibling          : 형제 관계에 있는 다음 값 (공백 포함)
# find_next_sibling     : 형제 관계에 있는 다음 값 (공백 미포함)
# previous_sibling      : 형제 관계에 있는 이전 값 (공백 포함)
# find_previous_sibling : 형제 관계에 있는 이전 값 (공백 미포함)
# parent                : 부모 관계에 있는 값
# find_all              : 맨 처음 발견되는 것뿐만 아니라 해당하는 전부 (list로 반환하므로 다음 코드에 인덱스 값 필요)

'''
status_code가 200이면 정상, 403이면 접근권한 없다는 뜻
status_code가 403이면 해당 서버에서 스크래핑 봇을 차단한 것이므로 사람인 척 접근하기 위해 User-Agent 처리 필요
'status_code가 200' = requests.codes.ok
'''

# 원본 URL 새 파일로 생성
with open("lotte_outer.html", "w", encoding="utf8") as f:
    f.write(res.text)

# 스크래핑한 것을 새 파일로 생성
with open("lotte_inner.html", "w", encoding="utf8") as f:
    f.write(str(inner))
'''