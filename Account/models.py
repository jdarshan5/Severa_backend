from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

# Validating the userid that it contains alphanumeric data and an underscore


def check_userid(userid):
    valid_characters = 'abcdefghijklmnopqsrtuvwxyz_0123456789'
    for char in userid:
        if not (char in valid_characters):
            raise ValidationError('Please enter valid userid containing letters [a-z, 0-9, _]')


class AccountManager(BaseUserManager):
    # Manager of our Custom Model.

    # Creating normal users.
    def create_user(self, userid, useremail, name, password=None):
        if not userid:
            raise ValueError('userid required.')
        if not useremail:
            raise ValueError('useremail required.')
        user = self.model(userid=userid,
                          useremail=self.normalize_email(useremail),
                          name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creating Super Users.
    def create_superuser(self, userid, useremail, name, password=None):
        user = self.create_user(userid=userid,
                                useremail=useremail,
                                name=name,
                                password=password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    Main Account which handles all the users of the platform.
        userid             : Unique Id of the user.                  E.g.: darshan_javiya
        useremail          : Email of the user.                      E.g.: abc@xyz.com
        userName           : Name of the user of his choice.         E.g.: Darshan Javiya
    """
    userid = models.CharField(max_length=100, unique=True, validators=[check_userid], null=False)
    useremail = models.EmailField(null=False)
    name = models.CharField(max_length=100, unique=False, null=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'userid'
    EMAIL_FIELD = 'useremail'
    REQUIRED_FIELDS = ['useremail', 'name']

    objects = AccountManager()

    def __str__(self):
        return self.userid

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
