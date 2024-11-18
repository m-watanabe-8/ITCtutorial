from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy

class MyNippoAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        resolved_url = super().get_login_redirect_url(request)  #settings.pyのLOGIN_REDIRECT_URL
        user_obj = request.user
        profile_obj = user_obj.profile
        # ログイン後にuserのemailとprofileのユーザ名が一致する場合(emailがユーザ名に設定されたままの場合)
        if user_obj.email == profile_obj.username:
            # profileの更新ページへ遷移
            resolved_url = reverse_lazy("profile-update", kwargs={"pk":profile_obj.pk})
        return resolved_url