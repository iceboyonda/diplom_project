from django.contrib import admin
from .models import TyreModel, TyreVariant, Favourite, Category, RimModel, RimVariant
from .forms import TyreModelForm, RimModelForm, TyreVariantFormSet, RimVariantFormSet

class TyreVariantInline(admin.TabularInline):
    model = TyreVariant
    extra = 1
    fields = ('width', 'profile', 'radius', 'season', 'studded', 'speed_index', 'price', 'stock', 'image')

@admin.register(TyreModel)
class TyreModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'get_radius_range', 'get_min_price', 'get_season_display', 'get_variants_count')
    list_filter = ('brand', 'variants__season', 'variants__studded')
    search_fields = ('brand', 'name', 'description', 'variants__width', 'variants__radius')
    ordering = ('brand', 'name')
    form = TyreModelForm
    inlines = [TyreVariantInline]

    def get_radius_range(self, obj):
        variants = obj.variants.all()
        radiuses = sorted(set(v.radius for v in variants if v.radius is not None))
        if not radiuses:
            return "—"
        ranges = []
        start = prev = radiuses[0]
        for r in radiuses[1:]:
            if r == prev + 1:
                prev = r
            else:
                if start == prev:
                    ranges.append(f'R{start}')
                else:
                    ranges.append(f'R{start}–R{prev}')
                start = prev = r
        if start == prev:
            ranges.append(f'R{start}')
        else:
            ranges.append(f'R{start}–R{prev}')
        return ", ".join(ranges)
    get_radius_range.short_description = "Радиусы"

    def get_min_price(self, obj):
        variants = obj.variants.all()
        prices = [v.price for v in variants if v.price is not None]
        return min(prices) if prices else "—"
    get_min_price.short_description = "Мин. цена"

    def get_season_display(self, obj):
        variants = obj.variants.all()
        if variants.exists():
            return variants[0].get_season_display()
        return "—"
    get_season_display.short_description = "Сезон"

    def get_variants_count(self, obj):
        return obj.variants.count()
    get_variants_count.short_description = "Кол-во вариантов"

class RimVariantInline(admin.TabularInline):
    model = RimVariant
    extra = 1
    fields = ('diameter', 'width', 'bolt_pattern', 'offset', 'dia', 'color', 'material', 'price', 'stock', 'image')

@admin.register(RimModel)
class RimModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'get_diameter_range', 'get_min_price', 'get_variants_count')
    list_filter = ('brand', 'variants__diameter', 'variants__material', 'variants__color')
    search_fields = ('brand', 'name', 'description', 'variants__bolt_pattern', 'variants__offset')
    ordering = ('brand', 'name')
    form = RimModelForm
    inlines = [RimVariantInline]

    def get_diameter_range(self, obj):
        variants = obj.variants.all()
        diameters = sorted(set(v.diameter for v in variants if v.diameter is not None))
        if not diameters:
            return "—"
        ranges = []
        start = prev = diameters[0]
        for d in diameters[1:]:
            if d == prev + 1:
                prev = d
            else:
                if start == prev:
                    ranges.append(f"{start}″")
                else:
                    ranges.append(f"{start}″–{prev}″")
                start = prev = d
        if start == prev:
            ranges.append(f"{start}″")
        else:
            ranges.append(f"{start}″–{prev}″")
        return ", ".join(ranges)
    get_diameter_range.short_description = "Диаметры"

    def get_min_price(self, obj):
        variants = obj.variants.all()
        prices = [v.price for v in variants if v.price is not None]
        return min(prices) if prices else "—"
    get_min_price.short_description = "Мин. цена"

    def get_variants_count(self, obj):
        return obj.variants.count()
    get_variants_count.short_description = "Кол-во вариантов"

@admin.register(TyreVariant)
class TyreVariantAdmin(admin.ModelAdmin):
    list_display = ('model', 'width', 'profile', 'radius', 'season', 'studded', 'speed_index', 'price', 'stock', 'is_in_stock')
    list_filter = ('model__brand', 'width', 'radius', 'season', 'studded', 'speed_index', 'price', 'stock')
    search_fields = ('model__brand', 'model__name', 'width', 'radius', 'speed_index')
    ordering = ('model__brand', 'model__name', 'width', 'profile', 'radius')
    list_editable = ('price', 'stock', 'studded')
    list_per_page = 20

    def is_in_stock(self, obj):
        return obj.stock > 0
    is_in_stock.boolean = True
    is_in_stock.short_description = "В наличии"

@admin.register(RimVariant)
class RimVariantAdmin(admin.ModelAdmin):
    list_display = ('model', 'diameter', 'width', 'bolt_pattern', 'offset', 'dia', 'color', 'material', 'price', 'stock', 'is_in_stock')
    list_filter = ('model__brand', 'diameter', 'width', 'bolt_pattern', 'material', 'color', 'price', 'stock')
    search_fields = ('model__brand', 'model__name', 'bolt_pattern', 'offset', 'color')
    ordering = ('model__brand', 'model__name', 'diameter', 'width')
    list_editable = ('price', 'stock', 'color', 'material')
    list_per_page = 20

    def is_in_stock(self, obj):
        return obj.stock > 0
    is_in_stock.boolean = True
    is_in_stock.short_description = "В наличии"
