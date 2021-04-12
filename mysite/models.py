from django.db import models
import uuid

from django.db.models.fields.related import ManyToManyField
# Create your models here.


#ユーザーモデルを読み取るため
from django.conf import settings
from django.utils import timezone

class Shop(models.Model):
    class Meta:
        db_table = "shop"

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="販売元", max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = "category"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="カテゴリー", max_length=10)

    def __str__(self):
        return self.name


class Products(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, verbose_name="カテゴリー", on_delete=models.PROTECT)
    shop = models.ForeignKey(
        Shop, verbose_name="販売元", on_delete=models.PROTECT)
    name = models.CharField(verbose_name="品名", max_length=30)
    price = models.IntegerField(verbose_name="価格")


    def __str__(self):
        return self.name





class Cart(models.Model):
    class Meta:
        db_table = "cart"

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product     = models.ForeignKey(Products,verbose_name="カゴに入っている商品",on_delete=models.CASCADE)
    amount      = models.PositiveIntegerField(verbose_name="数量",default=1)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="カゴの所有者",on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class History(models.Model):
    class Meta:
        db_table = "history"

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="決済日",default=timezone.now)
    product     = models.ForeignKey(Products,verbose_name="決済した商品",on_delete=models.CASCADE)
    amount      = models.PositiveIntegerField(verbose_name="決済した数量",default=1)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="決済した人",on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name



