from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .models import Profile
from .forms import ProfileUpdateForm
from utils.access_restrictions import OwnProfileOnly    # モジュール化したアクセス制限

# プロフィールの更新
class ProfileUpdateView(OwnProfileOnly, UpdateView):
    template_name = "accounts/profile-form.html"
    model = Profile
    form_class=ProfileUpdateForm
    success_url = reverse_lazy("nippo-list")