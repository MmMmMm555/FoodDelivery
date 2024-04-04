from django.contrib import admin

from .models import Category, Food, FoodImages


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 10


admin.site.register(Category, CategoryAdmin)


class FoodImagesAdmin(admin.TabularInline):
    model = FoodImages

# admin.site.register(FoodImages, FoodImagesAdmin)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'available',)
    list_editable = ('available',)
    search_fields = ('name',)
    list_filter = ('category__name', 'available',)
    list_per_page = 10
    inlines = [FoodImagesAdmin,]


admin.site.register(Food, FoodAdmin)
