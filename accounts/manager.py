from django.contrib.auth.models import BaseUserManager

class Usermanager(BaseUserManager):
    def create_user(self , username , password = None , **extra_field):
        if not username :
            raise ValueError('Username is required')
        
        if not password :
            raise ValueError("Password is required")
        
        
        username = self.model.normalize_username(username)
        extra_field.setdefault('is_active' , True)
        user = self.model(username = username , **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self , username , password= None  , **extra_field):
        extra_field.setdefault('is_staff' , True)
        extra_field.setdefault('is_superuser' , True)

        if extra_field.get('is_staff') is not True :
            raise ValueError ('Super user must have is_staff = True ')
        if extra_field.get('is_superuser') is not True :  
            raise ValueError ('Super user must have is_superuser = True ')
        return self.create_user(username,password,**extra_field)
       