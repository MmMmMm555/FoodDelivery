from modeltranslation.translator import TranslationOptions, register
from .models import Branch


@register(Branch)
class BranchTranslation(TranslationOptions):
    fields = ('name', 'address',)