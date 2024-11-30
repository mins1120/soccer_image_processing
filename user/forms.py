from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUp_Form(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SignUp_Form, self).__init__(*args, **kwargs)
        # 도움말 텍스트 제거
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "비밀번호가 일치하지 않습니다.")
            else:
                cleaned_data['password1'] = password1
                cleaned_data['password2'] = password2

        return cleaned_data

    def save(self, commit=True):
        user = super(SignUp_Form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])  # 패스워드를 암호화하여 저장
        if commit:
            user.save()
        return user