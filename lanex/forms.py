from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from lanex.models import Language, LanguageRequest, UserProfile, Comment
from location_field.forms.plain import PlainLocationField

'''
Form for adding a language, specifically for Superusers.
'''
class LanguageForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please add the name of the language.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Language
        fields = ('name',)


'''
Form for adding a request with the language specified, listing the fields provided for users 
  creating a request to complete.
'''
class RequestForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    desc = forms.CharField(widget=forms.Textarea)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_date = forms.DateTimeField(widget=forms.SelectDateWidget(), required=False)
    city = forms.CharField(max_length=255, help_text="Search Map", initial="Glasgow")
    location = PlainLocationField(based_fields=['city'], zoom=7, initial='55.87155490317328,-4.288530349731445', help_text="Move the pin around.")


    class Meta:
        model = LanguageRequest
        exclude = ('creator', 'slug', 'request_id','completed')

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    field_order = ['language','title', 'desc', 'views','suggested_date','city', 'location', 'picture']


'''
Alternative form for adding a request in the case where the language is already included due to
  being included in a different URL. In other words, adding a request designated to a pre-specified
  language to which the URL links.
'''
class LanguageRequestForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    desc = forms.CharField(widget=forms.Textarea)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    suggested_date = forms.DateTimeField(widget=forms.SelectDateWidget(), required=False)
    city = forms.CharField(max_length=255, help_text="Search Map", initial="Glasgow")
    location = PlainLocationField(based_fields=['city'], zoom=7, initial='55.87155490317328,-4.288530349731445', help_text="Move the pin around.")

    class Meta:
        model = LanguageRequest
        exclude = ('creator','slug','language','request_id','completed')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    field_order = ['title', 'desc', 'views', 'suggested_date', 'city', 'location', 'picture']

'''
Form for user registration. Users supply usually expected profile information. 
'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


'''
Form for user settings where a user may modify email, first and last name.
'''
class UserForm2(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','first_name','last_name')


'''
Form for user profile settings where a user can replace the default profile image with one of
  their own.
'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


'''
Form for adding comments.
'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)