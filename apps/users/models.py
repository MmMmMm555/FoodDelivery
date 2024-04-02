from django.db import models
from apps.branches.models import Branch
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    WAITER = 'waiter', _('waiter')
    CLIENT = 'client', _('client')


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), blank=True, unique=True)
    role = models.CharField(_("role"), max_length=6, choices=UserRoles.choices, default=UserRoles.CLIENT)
    branch = models.ForeignKey(Branch, verbose_name=_("branch"), related_name="waiters" , on_delete=models.SET_NULL, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []