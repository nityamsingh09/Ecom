from django.contrib import admin
from userauth.models import User, Profile,ContactUs

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'bio']


class ProfileAdmin(admin.ModelAdmin):
    list_display = [ 'user','full_name', 'bio', 'image', 'phone', 'verified']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'subject', 'message']
    


admin.site.register(User,UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)