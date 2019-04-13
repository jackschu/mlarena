from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.


class CustomUserManager(UserManager):
    def create_user(self, email, password, **fields):

        user = self.model(
            email=self.normalize_email(email),
            **fields,
        )
        user.username = user.email

        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['last_name', 'first_name']
    objects = CustomUserManager()
    def __str__(self):
        return self.username
    def get_full_name(self):
        return self.first_name + ' '+self.last_name
