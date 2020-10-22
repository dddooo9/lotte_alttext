from django.db import models


class Lotte(models.Model):
    p_id = models.CharField(max_length=10000, null=False)
    p_detail_url = models.CharField(max_length=10000, null=False)
    p_detail_inner_url = models.CharField(max_length=10000) # 상세보기 innerHtml URL 없을 수도 있음
    p_thumb_url = models.CharField(max_length=10000, null=False)
    p_brand = models.CharField(max_length=10000) # 브랜드 없을 수도 있음
    p_name = models.CharField(max_length=10000, null=False)
    p_price = models.CharField(max_length=10000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)