from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, null=False, blank=False)
    father_name = models.CharField(_("father name"), max_length=150, null=True, blank=True)
    email = models.EmailField(_("email address"), null=False, blank=False)
    phone_number = models.CharField(_("phone_number"), max_length=20, null=False, blank=False)
    job_title = models.CharField(_("job_title"), max_length=150, null=True, blank=True)
    # country = models.ForeignKey()
    is_moderator = models.BooleanField(_("is_moderator"), default=False)
    # company = models.ForeignKey()
    # subscription = models.ManyToManyField()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        app_label = 'accounts'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
