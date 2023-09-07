from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


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
    email = models.EmailField(_("email address"), null=False, blank=False)
    phone_number = PhoneNumberField(_("phone_number"), null=False, blank=False)
    job_title = models.CharField(_("job_title"), max_length=150, null=True, blank=True)
    # country = models.ForeignKey()
    is_moderator = models.BooleanField(_("is_moderator"), default=False)
    company = models.CharField(_('company_name'), max_length=150, null=True, blank=True)
    type_corp = models.IntegerField(_('company_type'), choices=TYPE_CORP_CHOICES)
    subscriptions = models.ManyToManyField(_("subscriptions"), related_name="users",
                                           through="subscription.user_subscription.UsersSubscription",
                                           through_fields=("user", "subscription"))

    def __str__(self):
        return f'{self.pk}. {self.get_full_name()}'

    class Meta:
        app_label = 'accounts'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
