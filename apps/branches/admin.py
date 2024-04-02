from django.contrib import admin

from .models import Branch



class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address',)
    search_fields = ('name', 'address',)
    list_per_page = 10

admin.site.register(Branch, BranchAdmin)