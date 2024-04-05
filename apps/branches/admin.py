from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Branch, BranchComments


class BranchCommentsAdmin(admin.TabularInline):
    model = BranchComments
    extra = 0
    readonly_fields = ('comment', 'client', 'branch',
                       'created_at', 'updated_at',)

    def has_add_permission(self, request, obj=None):
        return False

class BranchAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'address',)
    search_fields = ('name', 'address',)
    list_per_page = 10
    inlines = (BranchCommentsAdmin,)

admin.site.register(Branch, BranchAdmin)
