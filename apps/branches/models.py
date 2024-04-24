from django.db import models
from django.contrib.gis.db.models import PointField, PolygonField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.common.models import BaseModel
from apps.foods.models import Food
# from apps.users.models import User #noqa
from phonenumber_field.modelfields import PhoneNumberField


class Branch(BaseModel):
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
        verbose_name = _('Branch ')
        verbose_name_plural = _('Branches ')


class BranchComments(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_("branch"), related_name="comments")
    client = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("client"), related_name="branch_comments")
    rating = models.IntegerField(verbose_name=_("rating"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(verbose_name=_("comment"), null=True, blank=True)
    area = PolygonField(_("area"), geography=True, srid=4326, null=True, blank=True)

    def __str__(self):
        return self.client.first_name

    class Meta:
        db_table = "branch_comments"
        verbose_name = _("Branch comment ")
        verbose_name_plural = _("Branch comments ")
        unique_together = ("branch", "client")