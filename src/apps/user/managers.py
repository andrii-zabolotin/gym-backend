from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.phonenumber import PhoneNumber


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, email, first_name, last_name, sex, birth_date, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError(_("The Phone must be set"))

        if not email:
            raise ValueError(_("The Email must be set"))

        if not first_name:
            raise ValueError(_("The First Name must be set"))

        if not last_name:
            raise ValueError(_("The Last Namae must be set"))

        if not sex:
            raise ValueError(_("The Sex must be set"))

        if not birth_date:
            raise ValueError(_("The Birth Date must be set"))

        user = self.model(
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone, password, **extra_fields)
