from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "아이디"
        self.fields['email'].label = "이메일 주소"
        self.fields['password1'].label = "비밀번호"
        self.fields['password2'].label = "비밀번호 확인"
        self.fields['company_id'].label = "사업자 등록번호"
        self.fields['email'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'company_id']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 사용중인 이메일 주소입니다.")
        return email
