from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q 
from django.utils import timezone
from utils.random_string import random_string_generator

# ユーザーモデルクラスの取得
User = get_user_model()

# ランダムな新しい値を生成
def slug_maker():
    repeat = True
    while repeat:
        new_slug = random_string_generator()
        counter = NippoModel.objects.filter(slug=new_slug).count()
        if counter == 0:
            repeat = False
    return new_slug

# 検索　QuerySetクラス
class NippoModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        # qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            # タイトルかコンテントにQueryが含まれているものを絞り込み
            or_lookup = (
                Q(title__icontains=query)|
                Q(content__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("-date") #新しい順に並び替えてます
    
# get_querysetメソッドが呼び出された時にQuerySetクラスを使う
class NippoModelManager(models.Manager):
    def get_queryset(self):
        return NippoModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class NippoModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="タイトル")
    content = models.CharField(max_length=1000, verbose_name="内容")
    public = models.BooleanField(default=False, verbose_name="公開する")
    date = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=20, unique=True, default=slug_maker)
    timestamp = models.DateTimeField(auto_now_add=True)

    # 管理サイトの表記変更
    class Meta:
        verbose_name="日報"
        verbose_name_plural="日報一覧"

    objects = NippoModelManager()

    def __str__(self):
        return self.title
    
    def get_profile_page_url(self):
        from django.urls import reverse_lazy
        # リストビュー(html)の中のobjで使えるようになる
        return reverse_lazy("nippo-list") + f"?profile={self.user.profile.id}"


