from django.contrib import admin
from .models import TyreModel, TyreVariant, Favourite, Category, RimModel, RimVariant
from .forms import TyreModelForm, RimModelForm, TyreVariantFormSet, RimVariantFormSet

class TyreVariantInline(admin.TabularInline):
    model = TyreVariant
    extra = 1

@admin.register(TyreModel)
class TyreModelAdmin(admin.ModelAdmin):
    inlines = [TyreVariantInline]

class RimVariantInline(admin.TabularInline):
    model = RimVariant
    extra = 1
    fields = ('diameter', 'width', 'bolt_pattern', 'offset', 'dia', 'color', 'material', 'price', 'stock', 'image')

@admin.register(RimModel)
class RimModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')
    list_filter = ('brand',)
    search_fields = ('brand', 'name', 'description')
    ordering = ('brand', 'name')
    form = RimModelForm
    inlines = [RimVariantInline]

@admin.register(RimVariant)
class RimVariantAdmin(admin.ModelAdmin):
    list_display = ('model', 'diameter', 'width', 'bolt_pattern', 'price', 'stock')
    list_filter = ('model__brand', 'diameter', 'width', 'material')
    search_fields = ('model__brand', 'model__name', 'bolt_pattern', 'color')
    ordering = ('model__brand', 'model__name', 'diameter', 'width')
    list_editable = ('price', 'stock')

admin.site.register(TyreVariant)
