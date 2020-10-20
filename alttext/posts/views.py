from django.shortcuts import render

# Create your views here.
def shop(request):
    return render(request, 'posts/shop.html')

#상품 상세보기 페이지
