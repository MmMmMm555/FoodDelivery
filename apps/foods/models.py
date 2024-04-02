from django.db import models
from django.utils.translation import gettext_lazy as _



class Category(models.Model):
    name = models.CharField(_("name"), max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _('Category ')
        verbose_name_plural = _('Categories ')


class Food(models.Model):
    name = models.CharField(_("name"), max_length=100, blank=False, null=False)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name=_("category"), related_name='foods', on_delete=models.CASCADE)
    image = models.ImageField(_("image"), upload_to='foods/')
    available = models.BooleanField(_("available"), default=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _('Food ')
        verbose_name_plural = _('Foods ')
