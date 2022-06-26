from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from .models import Profile
from posts.models import PostComments



class LoginForm(AuthenticationForm):

    """ログオンフォーム"""
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "ユーザ名を入力"
        self.fields["password"].widget.attrs["placeholder"] = "パスワードを入力"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'display_name')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            

