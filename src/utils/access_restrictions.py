from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect

# ログインユーザーの日報だけアクセスできるよう制限
class OwnerOnly(UserPassesTestMixin):
    # アクセス制限を行う関数(ログインユーザー=データ作成者か)
    def test_func(self):
        nippo_instance = self.get_object()
        return nippo_instance.user == self.request.user
    
    # Falseの時のリダイレクト先を指定(アクセス拒否時)
    def handle_no_permission(self):
        messages.error(self.request, "ご自身の日報でのみ編集・削除可能です。")
        return redirect("nippo-detail", slug=self.kwargs["slug"])
    

# 自分のプロフィールしかアクセスできないように制限
class OwnProfileOnly(UserPassesTestMixin):
    def test_func(self):
        profile_obj = self.get_object()
        try:
            return profile_obj == self.request.user.profile
        except:
            return False