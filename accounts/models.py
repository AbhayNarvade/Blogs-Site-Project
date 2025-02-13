from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
from django.core.validators import MinLengthValidator
from .manager import Usermanager
# Create your models here.
class User (AbstractUser):
    id = models.UUIDField(primary_key= True , default= uuid.uuid4 , editable=False)
    username = models.CharField(max_length=50 , unique=True)
    password = models.CharField(max_length=50)
    mobileno = models.CharField(max_length=10, validators=[MinLengthValidator(10)] , unique=True )
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/' , blank=True , null= True)
    objects = Usermanager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email' , 'first_name' , 'last_name' , 'mobileno']

    def __str__(self):
        return f" {self.username}"
    
    def get_profile_image_url(self):
        """Return the profile image URL or a default image if not uploaded."""
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return "/static/images/default-profile.jpg"  # Replace with your actual default image path



class OTP(models.Model):
    id = models.UUIDField(primary_key= True , default= uuid.uuid4 , editable=False)
    code = models.CharField(max_length=6 )
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='otps')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} :-  {self.code}"     