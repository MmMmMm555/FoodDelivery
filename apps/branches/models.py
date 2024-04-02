from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(_("name"), max_length=100, blank=False, null=False)
    address = models.CharField(_("address"), max_length=200, blank=False, null=False)
    longitude = models.FloatField(_("longitude"))
    latitude = models.FloatField(_("latitude"))

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Branch '
        verbose_name_plural = 'Branches '