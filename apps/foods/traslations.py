from modeltranslation.translator import TranslationOptions, register
from .models import Food, Category


@register(Food)
class FoodTranslation(TranslationOptions):
    fields = ('name',)


@register(Category)
class FoodTranslation(TranslationOptions):
    fields = ('name',)