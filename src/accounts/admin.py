from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User,Profile
from .forms import CustomAdminChangeForm

class UserAdmin(BaseUserAdmin):
    form = CustomAdminChangeForm
    # user一覧の表示を変える
    list_display = (
        "email",
        "active",
        "staff",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
    )
    ordering = ("email",)
    filter_horizontal = ()

    # 検索バーの検索対象
    search_fields = ('email',)

    # user追加のフィールドを指定
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    # 編集ページのフィールドを指定
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('プロフィール', {'fields': (
            'username',
            'department',
            'phone_number',
            'gender',
            'birthday',
        )}),
        ('権限', {'fields': ('staff','admin',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)