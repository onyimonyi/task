from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,
                    is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have surname and other names")
        user_obj = self.model(
            email=self.normalize_email(email),
            username=username,

        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, username, email, password=None):
        user = self.create_user(
            email,
            username,

            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email,
            username,

            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin



class Task(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100,  blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']