from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.db.models.signals import post_save

GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]

# マネージャークラス(データを取得するメソッドを自作できる)
# 既存のクラスを上書きして専用のユーザーモデルにする
class UserManager(BaseUserManager):
    # create_userをベースに他の権限を作成
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('ユーザー登録にはメールアドレスが必要です。')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)  # アクティブか
    staff = models.BooleanField(default=False)  # スタッフか
    admin = models.BooleanField(default=False)  # 管理者か

    USERNAME_FIELD = 'email'    # メールアドレスでログイン

    # モデルマネジャー「UserManger」とモデル「User」を紐付け
    objects = UserManager()

    def __str__(self):             
        return self.email

    def has_perm(self, perm, obj=None): # 管理者か
        return self.admin

    def has_module_perms(self, app_label):  # モジュールの権限
        return self.admin

    # @propertyでプロパティとして属性を設定
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
# プロフィール　
class Profile(models.Model):
    # Userモデルクラスと1:1で紐づく
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, verbose_name="ユーザー名")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部署")
    phone_number = models.IntegerField(blank=True, null=True, verbose_name="携帯番号")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, verbose_name="性別", blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")

    def __str__(self):
        return self.username
    
    def get_own_archive_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("nippo-list") + f"?profile={self.id}"
    
# ユーザー作成時に実行される関数
def post_user_created(sender, instance, created, **kwargs):
    # 新規登録時のみ実行
    if created:
        profile_obj = Profile(user=instance)    # instanceはユーザーモデルクラスの新しく追加されたレコード
        profile_obj.username = instance.email
        profile_obj.save()

post_save.connect(post_user_created, sender=User)   # Signalと関数を結びつける(Userのsaveメソッドの後実行)