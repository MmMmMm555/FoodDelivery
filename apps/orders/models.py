from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models import PointField
from datetime import timedelta

from apps.common.models import BaseModel
from apps.users.models import User
from apps.branches.models import Branch
from apps.foods.models import Food


class PaymentTypes(models.TextChoices):
    CASH = "cash", _("cash")
    CARD = "card", _("card")


class States(models.TextChoices):
    WAITING = "waiting", _("waiting")
    PREPARING = "preparing", _("preparing")
    DELIVERING = "delivering", _("delivering")
    CANCELLED = "cancelled", _("cancelled")

class Order(BaseModel):
    client = models.ForeignKey(User, verbose_name=_(
        "client"), on_delete=models.CASCADE)
    total_price = models.DecimalField(
        _("total price"), max_digits=10, decimal_places=2, default=0)
    payment_type = models.CharField(
        _("payment type"), max_length=4, choices=PaymentTypes.choices, default=PaymentTypes.CASH)
    state = models.CharField(_("state"), max_length=10,
                             choices=States.choices, default=States.WAITING)
    location = PointField(_("location"), geography=True, srid=4326)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="orders", verbose_name=_("branch"))
    delivery_time = models.DurationField(
        _("delivery time"), default=timedelta(minutes=3))

    def __str__(self):
        return self.client.email

    class Meta:
        db_table = 'orders'
        verbose_name = _('Order ')
        verbose_name_plural = _('Orders ')


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("order"))
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name="orders", verbose_name=_("food"))
    amount = models.PositiveIntegerField(
        _("amount"), blank=False, null=False, default=1)
    total_price = models.DecimalField(
        _("total price"), max_digits=10, decimal_places=2)
    comment = models.TextField(_("comment"), blank=True, null=True)

    def __str__(self) -> str:
        return self.food.name

    class Meta:
        db_table = 'order_items'
        verbose_name = _('Order Item ')
        verbose_name_plural = _('Order Items ')
