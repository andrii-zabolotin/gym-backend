from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from apps.user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    SEX_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
    ]

    phone = PhoneNumberField(unique=True, verbose_name=_("Phone number"))
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("E-mail"))
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name=_("Sex"))
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Registration date")
    )
    date_edited = models.DateTimeField(
        auto_now=True, verbose_name=_("Editing date")
    )
    birth_date = models.DateField(verbose_name=_("Birthday date"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_massagist = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return str(self.phone)
