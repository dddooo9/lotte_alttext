import re

# 스크랩하고자 하는 형태
p = re.compile("..se$")

# ca.e  : .에 들어갈 단 하나의 문자를 의미
# ^de   : de로 시작하는 문자열을 의미
# se$   : se로 끝나는 문자열을 의미

# 컴파일한 것과 매칭
m = p.search("asdasdf asdf coffee and doughnut cake cafe care case")

# match()   : 문자열 첫 부분에서 일치하는 것 단일 확인
# search()  : 문자열 첫 부분이 아니더라도 일치하는 것 단일 확인
# findall() : 문자열 첫 부분이 아니더라도 일치하는 것 복수 확인 (list로 반환하므로 print attribute 불필요)

# 매칭(반환)된 것 출력
print(m.group())

# m.group() : 일치하는 문자열 반환
# m.string  : 입력받은 문자열 자체 반환
# m.start() : 일치하는 문자열의 시작 index 반환
# m.end()   : 일치하는 문자열의 끝 index 반환
# m.span()  : 일치하는 문자열의 (시작, 끝) index 반환