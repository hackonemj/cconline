from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_condutor = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    funcionario_id = models.IntegerField('Nº do Funcionário', unique=True, null=True)

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)
