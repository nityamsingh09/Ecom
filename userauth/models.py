from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username= models.CharField(max_length=100)
    bio = models.CharField( max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # when creating superuser, Django will ask for username

    def __str__(self):
        return self.username
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    image =models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=100,null=True)
    bio = models.TextField(max_length=200,null=True)
    phone = models.CharField(max_length=15,null=True)
    verified =models.BooleanField(default=True)

    def __str__(self): 
        return self.user.username
        


class ContactUs(models.Model):
    full_name = models.CharField( max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us "
        

    def __str__(self):
        return self.full_name
   
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)