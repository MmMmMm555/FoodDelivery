from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class OrderField(models.IntegerField):
    def __init__(self, verbose_name=_("Order"), default=1, validators=None, **kwargs):
        if validators is None:
            validators = [MinValueValidator(1)]
        super().__init__(verbose_name=verbose_name, default=default, validators=validators, **kwargs)

