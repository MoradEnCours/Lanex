from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from lanex.models import Language, LanguageRequest, UserProfile, Comment

class LanguageForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please add the name of the language.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Language
        fields = ('name',)

class RequestForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please include the title.")
    desc = forms.CharField(widget=forms.Textarea)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_date = forms.DateTimeField(widget=forms.SelectDateWidget(), required=False)
    city = forms.CharField(max_length=255, help_text="Search Map", initial="Glasgow")

    class Meta:
        model = LanguageRequest
        exclude = ('language', 'slug', 'request_id','completed')

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    field_order = ['language','title', 'desc', 'views','suggested_date','city','picture']

class LanguageRequestForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    desc = forms.CharField(widget=forms.Textarea)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_date = forms.DateTimeField(widget=forms.SelectDateWidget(), required=False)
    city = forms.CharField(max_length=255, help_text="Search Map", initial="Glasgow")

    class Meta:
        model = LanguageRequest
        exclude = ('creator','slug','language','request_id','completed')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    field_order = ['title', 'desc', 'views','suggested_date','city','picture']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserForm2(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)