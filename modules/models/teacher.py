from django.db import models
from django.utils.translation import gettext_lazy as _

from modules.models.module import AbstractModel


class TeacherModel(AbstractModel):
    first_name = models.CharField(_('First name'), max_length=40, null=False, blank=False)
    last_name = models.CharField(_('Last name'), max_length=40, null=False, blank=False)
    father_name = models.CharField(_('Father name'), max_length=40, null=True, blank=True)
    job_title = models.CharField(_('Job title'), max_length=150, null=True, blank=True)
    corp = models.CharField(_('Company'), max_length=150, null=True, blank=True)
    experience = models.CharField(_('Experience'), max_length=150, null=True, blank=True)
    description = models.TextField(_('About teacher'), max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'teacher'
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.father_name:
            full_name = "%s %s %s" % (self.first_name, self.last_name, self.father_name)
            return full_name.strip()
        else:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()

