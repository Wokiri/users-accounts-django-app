from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LibraryUser(models.Model):

    class Sections(models.TextChoices):
        ADVENTURE = 'ADV', _('Adventure')
        REALITY = 'REAL', _('Real')
        EDUCATION = 'EDU', _('Education')


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_section = models.CharField(_('favorite section'), max_length=5, choices=Sections.choices)
    is_administrator = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)



    def __str__(self):
        return (f'{self.user.first_name} ({self.user.email})')