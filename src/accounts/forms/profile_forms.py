from django import forms
from accounts.models import Profile

# プロフィール編集
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    # user名のバリデーションチェック
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_email = self.instance.user.email
        if username == user_email:
            raise forms.ValidationError("ユーザー名を変更してください")
        elif "@" in username:   # バリデーションとしては弱い
            raise forms.ValidationError("ユーザー名にEメールアドレスは使用できません")
        return username