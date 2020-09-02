from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
# from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from datetime import datetime



class UserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError(_("Users must have an phone address"))
        # email = self.normalize_email(email)
        user = self.model(phone=phone)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password,**extra_fields):
        user = self.create_user(phone)
        # user.is_active = True
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        # user.role = User.ROLE_ADMINISTRATOR
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone, password=password, is_staff=True, is_active=True)
        return user


def user_photos_dir(instanse, filename):
    usrnme = f'{instanse.phone}'
    folder_name = f"{usrnme}/{datetime.today().strftime('%d_%m_%Y')}/{filename}"
    return folder_name


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_SALES_DEPARTMENT = 1
    ROLE_CONTROL_DEPARTMENT = 2
    ROLE_CHOICES = (
        (ROLE_SALES_DEPARTMENT, 'Отдел продаж'),
        (ROLE_CONTROL_DEPARTMENT, 'Отдел контроля')
    )


    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
    # message = "Phone number in the format '+77777777'. Up to 12 digits")
    # phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password1 = models.CharField(max_length=20, blank=True, null=True)
    password2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True,
                                auto_now=False,
                                auto_now_add=False)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,
                                      null=True, blank=True)

    # ------------------------------------------------------
    country = models.ForeignKey("locations.Country", on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey("locations.Region", on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey("locations.City", on_delete=models.CASCADE, blank=True, null=True)


    # -------------------------------------------------------
    # like = models.ManyToManyField("self", blank=True, related_name="likes")
    # dislike = models.ManyToManyField("self", blank=True, related_name="dislikes")


    # first_name = models.CharField(max_length=255, blank=True, null=True)
    # last_name = models.CharField(max_length=255, blank=True, null=True)
    # middle_name = models.CharField(max_length=255, blank=True, null=True)

    # -------------------------------------------------------
    role = models.SmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    # -------------------------------------------------------
    # role = models.ManyToManyField(SubRole, related_name = "role_user", blank=True)

    #--------------------------------------------------------
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_checked = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)

    #--------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(null=True, blank=True)
     
    #--------------------------------------------------------
    avatar = models.ImageField(upload_to=user_photos_dir, default="default/default.png")
    # ava = models.TextField(blank=True, null=True)
    # front_passport = models.ImageField(upload_to=user_photos_dir, blank=True, null=True)
    # back_passport = models.ImageField(upload_to=user_photos_dir, blank=True, null=True)

    #--------------------------------------------------------
    # rating_array = ArrayField(models.FloatField(null=True, blank=True, 
    #                           validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]), null=True ,blank=True, default=list,
    #                          )
    # rat = models.FloatField(blank=True, null=True)

    # about = models.TextField(blank=True, null=True)
    favorites = models.ManyToManyField("products.Product", related_name="favs", blank=True)
    basket = models.ManyToManyField("products.Product", related_name="basket", blank=True)

    # -------------------------------------------------------
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.id) + ", " + self.phone

    # def rating(self):
    #     sum_r = 0
    #     rat = 0
    #     if self.rating_array:
    #         for i in self.rating_array:
    #             sum_r += i
    #             rat = sum_r / len(self.rating_array)
    #         return rat
    #     else:
    #         return rat



class PhoneOTP(models.Model):
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
    # message = "Phone number in the format '+77777777'. Up to 12 digits")
    # phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    phone = models.CharField(max_length = 12, unique = True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    validated = models.BooleanField(default=False, help_text = 'True means user has a validated otp correctly in second API')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
