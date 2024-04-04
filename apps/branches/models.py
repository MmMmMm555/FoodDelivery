from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.translation import gettext_lazy as _

from apps.foods.models import Food
from phonenumber_field.modelfields import PhoneNumberField


class Branch(models.Model):
    name = models.CharField(_("name"), max_length=100)
    address = models.CharField(_("address"), max_length=200)
    branch_contact = PhoneNumberField(_("branch_contact"))
    location = PointField(_("location"), geography=True, srid=4326, null=True)
    branch_foods = models.ManyToManyField(Food, verbose_name=_(
        "branch_foods"), related_name='branch_foods')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'branches'
        verbose_name = 'Branch '
        verbose_name_plural = 'Branches '
