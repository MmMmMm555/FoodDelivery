from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, Food, FoodImages


class CategoryFoodsAdmin(admin.TabularInline):
    model = Food
    extra = 0


class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 10
    inlines = (CategoryFoodsAdmin,)


admin.site.register(Category, CategoryAdmin)


class FoodImagesAdmin(admin.TabularInline):
    model = FoodImages
    extra = 0


class FoodAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'price', 'category', 'available',)
    list_editable = ('available',)
    search_fields = ('name',)
    list_filter = ('category__name', 'available',)
    list_per_page = 10
    inlines = (FoodImagesAdmin,)


admin.site.register(Food, FoodAdmin)
