from django import forms
from django.contrib.auth.models import User
from lanex.models import Language, LanguageRequest, UserProfile

class LanguageForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please add the name of the language.")
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Language
        fields = ('name',)

class RequestForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please include the title.")
    url = forms.URLField(max_length=200, help_text="Please input the URL.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = LanguageRequest
        exclude = ('language',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserForm2(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

