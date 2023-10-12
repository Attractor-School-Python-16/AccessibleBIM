from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        username = email
        extra_fields['email_verified'] = True

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ENTREPRENEUR = 1
    LIMITED_LIABILITY_COMPANY = 2
    OPENED_JOINT_STOCK_COMPANY = 3
    CLOSED_JOINT_STOCK_COMPANY = 4
    ADDITIONAL_LIABILITY_COMPANY = 5
    STATE_COMPANY = 6
    OTHER = 7
    TYPE_CORP_CHOICES = [
        (ENTREPRENEUR, _("entrepreneur")),
        (LIMITED_LIABILITY_COMPANY, _("limited_liability_company")),
        (OPENED_JOINT_STOCK_COMPANY, _("opened joint stock company")),
        (CLOSED_JOINT_STOCK_COMPANY, _("closed joint stock company")),
        (ADDITIONAL_LIABILITY_COMPANY, _("additional liability company")),
        (STATE_COMPANY, _("state company")),
        (OTHER, _("other typecorp")),
    ]

    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    father_name = models.CharField(_("father name"), max_length=150, null=True, blank=True)
    email = models.EmailField(_("email address"), null=False, blank=False, unique=True)
    email_verified = models.BooleanField(_("email_verified"), default=False)
    phone_number = PhoneNumberField(_("phone_number"), null=False, blank=False)
    job_title = models.CharField(_("job_title"), max_length=150, null=True, blank=True)
    country = CountryField(_("country"), blank_label=_('select country'))
    company = models.CharField(_('company_name'), max_length=150, null=True, blank=True)
    type_corp = models.IntegerField(_('company_type'), choices=TYPE_CORP_CHOICES, default=7)
    subscriptions = models.ManyToManyField("subscription.SubscriptionModel", related_name="users",
                                           through="subscription.UsersSubscription",
                                           through_fields=("user", "subscription"))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.pk}. {self.get_full_name()}'

    class Meta:
        app_label = 'accounts'
        permissions = (
            ("can_view_admin_panel ", "Can view admin panel"),
            ("can_grant_moderator_role", "Can grant moderator role to other users"),
        )

    def is_moderator(self):
        return self.groups.filter(name='moderators').exists()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
