from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):

    def __str__(self):
        return self.get_full_name()