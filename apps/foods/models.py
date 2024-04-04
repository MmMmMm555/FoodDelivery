from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(_("name"), max_length=100)
    image = models.ImageField(_("images"), upload_to='category_images/')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = _('Category ')
        verbose_name_plural = _('Categories ')


class Food(BaseModel):
    name = models.CharField(_("name"), max_length=100)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name=_(
        "category"), related_name='foods', on_delete=models.CASCADE)
    available = models.BooleanField(_("available"), default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "foods"
        verbose_name = _('Food ')
        verbose_name_plural = _('Foods ')


class FoodImages(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images', verbose_name=_('food_image'))
    image = models.ImageField(_("image"), upload_to='food_images/', blank=False,)

    def __str__(self) -> str:
        return self.food.name

    class Meta:
        db_table = "food_images"
        verbose_name = _('Food image ')
        verbose_name_plural = _('Food images ')
    