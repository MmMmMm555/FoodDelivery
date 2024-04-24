from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.contrib.gis.admin import GISModelAdmin

from .models import Branch, BranchComments


# class BranchCommentsAdmin(admin.TabularInline):
#     model = BranchComments
#     extra = 0
#     readonly_fields = ('comment', 'client', 'branch',
#                        'created_at', 'updated_at',)

#     def has_add_permission(self, request, obj=None):
#         return False

class BranchAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'address',)
    search_fields = ('name', 'address',)
    list_per_page = 10
    # inlines = (BranchCommentsAdmin,)

admin.site.register(Branch, BranchAdmin)

class BranchCommentsAdmin(GISModelAdmin):
    list_display = ('id', 'branch', 'client', 'rating', 'comment', 'area', 'created_at', 'updated_at',)
    search_fields = ('branch', 'client', 'rating',)
    list_per_page = 10

admin.site.register(BranchComments, BranchCommentsAdmin)