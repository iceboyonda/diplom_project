from django.contrib import admin
from .models import TyreModel, TyreVariant

class TyreVariantInline(admin.TabularInline):
    model = TyreVariant
    extra = 1

@admin.register(TyreModel)
class TyreModelAdmin(admin.ModelAdmin):
    inlines = [TyreVariantInline]

admin.site.register(TyreVariant)
