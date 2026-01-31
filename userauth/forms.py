from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User, Profile

class UserRegisterForm(UserCreationForm):
    username= forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email= forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password1= forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2= forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Full Name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone Number'}))
    image = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Bio','rows':4}), required=False)
    

    class Meta:
        model = Profile
        fields = ['full_name',  'phone', 'image', 'bio'] 