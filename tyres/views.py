from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db.models.functions import Lower
from .models import TyreModel, TyreVariant, Favourite, RimModel, RimVariant, FavouriteRim
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from urllib.parse import urlencode
from .forms import TyreModelForm, TyreVariantFormSet
from django.views.decorators.http import require_POST
from django.contrib import messages

def annotate_tyres(tyres):
    for tyre in tyres:
        variants = list(tyre.variants.all())
        # Диапазон радиусов
        radiuses_list = sorted(set(v.radius for v in variants if v.radius is not None))
        ranges = []
        if radiuses_list:
            start = prev = radiuses_list[0]
            for r in radiuses_list[1:]:
                if r == prev + 1:
                    prev = r
                else:
                    if start == prev:
                        ranges.append(f'R{start}')
                    else:
                        ranges.append(f'R{start}-R{prev}')
                    start = prev = r
            if start == prev:
                ranges.append(f'R{start}')
            else:
                ranges.append(f'R{start}-R{prev}')
            tyre.radius_range = ', '.join(ranges)
        else:
            tyre.radius_range = '—'
        # Минимальная цена
        prices = [v.price for v in variants if v.price is not None]
        tyre.min_price = min(prices) if prices else None
        # Сезон
        tyre.season_display = variants[0].get_season_display() if variants else '—'
    return tyres

def annotate_rims(rims):
    for rim in rims:
        variants = list(rim.variants.all())
        # Диапазон диаметров и ширин
        diameters = sorted(list(set(v.diameter for v in variants if v.diameter is not None)))
        widths = sorted(list(set(v.width for v in variants if v.width is not None)))
        bolt_patterns_list = sorted(list(set(v.bolt_pattern for v in variants if v.bolt_pattern is not None and v.bolt_pattern != '')))
        
        rim.diameter_display = ', '.join(str(d) for d in diameters) if diameters else '—'
        rim.width_display = ', '.join(str(w) for w in widths) if widths else '—'
        rim.bolt_patterns_display = ', '.join(bolt_patterns_list) if bolt_patterns_list else '—'

        # Минимальная цена
        prices = [v.price for v in variants if v.price is not None]
        rim.min_price = min(prices) if prices else None
    return rims

def catalogue(request):
    tyres = TyreModel.objects.prefetch_related('variants').all()
    
    # Фильтрация по параметрам
    brand = request.GET.get('brand')
    if brand:
        tyres = tyres.filter(brand=brand)
    width = request.GET.get('width')
    if width:
        tyres = tyres.filter(variants__width=width)
    profile = request.GET.get('profile')
    if profile:
        tyres = tyres.filter(variants__profile=profile)
    radius = request.GET.get('radius')
    if radius:
        tyres = tyres.filter(variants__radius=radius)
    season = request.GET.get('season')
    if season:
        tyres = tyres.filter(variants__season=season)
    studded = request.GET.get('studded')
    if studded:
        tyres = tyres.filter(variants__studded=True)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if max_price:
        min_price = min_price or 0
        tyres = tyres.filter(variants__price__range=(min_price, max_price))
    elif min_price:
        tyres = tyres.filter(variants__price__gte=min_price)
    
    # Поиск по названию
    query = request.GET.get('q')
    if query:
        tyres = tyres.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    
    tyres = tyres.distinct()
    
    # Пагинация
    paginator = Paginator(tyres, 6)  # 6 шин на страницу (2 в ряд, 3 ряда)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    annotate_tyres(page_obj.object_list)
    
    # Собираем query_string для фильтров (кроме page)
    filter_params = request.GET.copy()
    if 'page' in filter_params:
        filter_params.pop('page')
    query_string = ''
    if filter_params:
        query_string = '&' + urlencode(filter_params, doseq=True)
    
    brands = TyreModel.objects.values_list('brand', flat=True).distinct()
    brands = sorted(set(b.strip().capitalize() for b in brands if b))
    widths = sorted(set(TyreVariant.objects.values_list('width', flat=True).distinct()))
    profiles = sorted(set(TyreVariant.objects.values_list('profile', flat=True).distinct()))
    radiuses = sorted(set(TyreVariant.objects.values_list('radius', flat=True).distinct()))
    
    context = {
        'page_obj': page_obj,
        'tyres': page_obj.object_list,
        'brands': brands,
        'widths': widths,
        'profiles': profiles,
        'radiuses': radiuses,
        'seasons': dict(TyreVariant.SEASON_CHOICES),
        'query_string': query_string,
        'selected_brand': brand,
        'selected_width': width,
        'selected_profile': profile,
        'selected_radius': radius,
        'selected_season': season,
        'selected_studded': studded,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
    }
    
    # Если HTMX-запрос — возвращаем только partial
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'tyres/_tyres_list.html', context)
    return render(request, 'tyres/catalogue.html', context)

def tyre_detail(request, tyre_id):
    tyre = get_object_or_404(TyreModel, id=tyre_id)
    variants = tyre.variants.all()
    widths = sorted(set(v.width for v in variants))
    profiles = sorted(set(v.profile for v in variants))
    radiuses = sorted(set(v.radius for v in variants))
    speed_indexes = sorted(set(v.speed_index for v in variants))
    seasons = sorted(set(v.get_season_display() for v in variants))
    studded = any(v.studded for v in variants)
    favourite_ids = []
    if request.user.is_authenticated:
        favourite_ids = list(request.user.favourites.filter(variant__in=variants).values_list('variant_id', flat=True))
    return render(request, 'tyres/tyre_detail.html', {
        'tyre': tyre,
        'variants': variants,
        'widths': widths,
        'profiles': profiles,
        'radiuses': radiuses,
        'speed_indexes': speed_indexes,
        'seasons': seasons,
        'studded': studded,
        'favourite_ids': favourite_ids,
    })

def search_tyres(request):
    query = request.GET.get('q')
    if query:
        tyres = TyreModel.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        tyres = TyreModel.objects.all()
    
    annotate_tyres(tyres) # Аннотируем результаты поиска шин
    
    return render(request, 'tyres/catalogue.html', {'tyres': tyres, 'query': query}) # Возвращаем на страницу каталога шин

def faq(request):
    return render(request, 'tyres/faq.html')

@login_required
def add_favourite(request, variant_id):
    variant = get_object_or_404(TyreVariant, id=variant_id)
    Favourite.objects.get_or_create(user=request.user, variant=variant)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_favourite(request, variant_id):
    variant = get_object_or_404(TyreVariant, id=variant_id)
    Favourite.objects.filter(user=request.user, variant=variant).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def favourites(request):
    favourite_tyre_variants = TyreVariant.objects.filter(favourited_by__user=request.user).select_related('model')
    favourite_rim_variants = RimVariant.objects.filter(favourited_by_rims__user=request.user).select_related('model')
    
    # Отладочный вывод (можно будет убрать после проверки)
    print(f'[DEBUG] favourites view: Number of favourite tyre variants for user {request.user.username}: {favourite_tyre_variants.count()}')
    print(f'[DEBUG] favourites view: Number of favourite rim variants for user {request.user.username}: {favourite_rim_variants.count()}')
    
    return render(request, 'tyres/favourites.html', {
        'favourite_tyre_variants': favourite_tyre_variants,
        'favourite_rim_variants': favourite_rim_variants,
    })

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_tyres(request):
    tyres = TyreModel.objects.prefetch_related('variants').all()
    annotate_tyres(tyres)
    return render(request, 'tyres/admin_tyres.html', {'tyres': tyres})

@user_passes_test(lambda u: u.is_staff)
def admin_tyre_add(request):
    if request.method == 'POST':
        form = TyreModelForm(request.POST, request.FILES)
        formset = TyreVariantFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            tyre = form.save()
            formset.instance = tyre
            formset.save()
            return redirect('tyres:admin_tyres')
    else:
        form = TyreModelForm()
        formset = TyreVariantFormSet()
    return render(request, 'tyres/admin_tyre_add.html', {'form': form, 'formset': formset})

@user_passes_test(lambda u: u.is_staff)
def admin_tyre_edit(request, tyre_id):
    tyre = get_object_or_404(TyreModel, id=tyre_id)
    if request.method == 'POST':
        form = TyreModelForm(request.POST, request.FILES, instance=tyre)
        if form.is_valid():
            form.save()
            return redirect('tyres:admin_tyres')
    else:
        form = TyreModelForm(instance=tyre)
    return render(request, 'tyres/admin_tyre_edit.html', {'form': form, 'tyre': tyre})

@user_passes_test(lambda u: u.is_staff)
def admin_tyre_delete(request, tyre_id):
    tyre = get_object_or_404(TyreModel, id=tyre_id)
    if request.method == 'POST':
        tyre.delete()
        return redirect('tyres:admin_tyres')
    return render(request, 'tyres/admin_tyre_delete.html', {'tyre': tyre})

@user_passes_test(lambda u: u.is_staff)
def admin_categories(request):
    # Здесь будет логика для категорий
    return render(request, 'tyres/admin_categories.html')

def rim_list(request):
    print(f"[DEBUG] rim_list: Получены GET параметры: {request.GET}")
    # Получаем все параметры фильтрации
    diameters = request.GET.getlist('diameter')
    widths = request.GET.getlist('width')
    bolt_patterns = request.GET.getlist('bolt_pattern')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    query = request.GET.get('q')
    brand = request.GET.get('brand')
    material = request.GET.get('material')
    color = request.GET.get('color')

    rims = RimModel.objects.prefetch_related('variants').all()
    print(f"[DEBUG] rim_list: Начальный queryset (все диски): {rims.count()} шт.")

    # Фильтрация
    if diameters:
        rims = rims.filter(variants__diameter__in=diameters)
        print(f"[DEBUG] rim_list: После фильтрации по диаметру ({diameters}): {rims.count()} шт.")
    if widths:
        rims = rims.filter(variants__width__in=widths)
        print(f"[DEBUG] rim_list: После фильтрации по ширине ({widths}): {rims.count()} шт.")
    if bolt_patterns:
        rims = rims.filter(variants__bolt_pattern__in=bolt_patterns)
        print(f"[DEBUG] rim_list: После фильтрации по креплению ({bolt_patterns}): {rims.count()} шт.")
    if max_price:
        min_price = min_price or 0
        rims = rims.filter(variants__price__range=(min_price, max_price))
        print(f"[DEBUG] rim_list: После фильтрации по цене ({min_price}-{max_price}): {rims.count()} шт.")
    elif min_price:
        rims = rims.filter(variants__price__gte=min_price)
        print(f"[DEBUG] rim_list: После фильтрации по минимальной цене ({min_price}): {rims.count()} шт.")
    if brand:
        rims = rims.filter(brand=brand)
        print(f"[DEBUG] rim_list: После фильтрации по бренду ({brand}): {rims.count()} шт.")
    if material:
        rims = rims.filter(variants__material=material)
        print(f"[DEBUG] rim_list: После фильтрации по материалу ({material}): {rims.count()} шт.")
    if color:
        rims = rims.filter(variants__color=color)
        print(f"[DEBUG] rim_list: После фильтрации по цвету ({color}): {rims.count()} шт.")

    # Поиск
    if query:
         rims = rims.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
         print(f"[DEBUG] rim_list: После поиска по запросу \"{query}\": {rims.count()} шт.")

    rims = rims.distinct()
    print(f"[DEBUG] rim_list: После distinct(): {rims.count()} шт.")

    # Пагинация
    print(f"[DEBUG] rim_list: Конечный queryset перед пагинацией: {rims.count()} шт.")
    paginator = Paginator(rims, 6)  # 6 дисков на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    annotate_rims(page_obj.object_list)

    # Параметры для фильтров
    available_diameters = sorted(list(set(RimVariant.objects.values_list('diameter', flat=True))))
    available_widths = sorted(list(set(RimVariant.objects.values_list('width', flat=True))))
    available_bolt_patterns = sorted(list(set(RimVariant.objects.values_list('bolt_pattern', flat=True).exclude(bolt_pattern=''))))

    # Сохраняем выбранные фильтры для формы
    selected_diameters = diameters
    selected_widths = widths
    selected_bolt_patterns = bolt_patterns
    selected_min_price = min_price
    selected_max_price = max_price

    brands = RimModel.objects.values_list('brand', flat=True).distinct()
    brands = sorted(set(b.strip().capitalize() for b in brands if b))
    materials = sorted(set(RimVariant.objects.values_list('material', flat=True).distinct()))
    colors = sorted(set(RimVariant.objects.values_list('color', flat=True).distinct()))
    context = {
        'page_obj': page_obj,
        'rims': page_obj.object_list,
        'available_diameters': available_diameters,
        'available_widths': available_widths,
        'available_bolt_patterns': available_bolt_patterns,
        'selected_diameters': selected_diameters,
        'selected_widths': selected_widths,
        'selected_bolt_patterns': selected_bolt_patterns,
        'selected_min_price': selected_min_price,
        'selected_max_price': selected_max_price,
        'query': query, # Передаем поисковый запрос
        'brands': brands,
        'materials': materials,
        'colors': colors,
        'selected_brand': brand,
        'selected_material': material,
        'selected_color': color,
    }

    # Собираем query_string для фильтров (кроме page)
    filter_params = request.GET.copy()
    if 'page' in filter_params:
        filter_params.pop('page')
    query_string = ''
    if filter_params:
        query_string = '&' + urlencode(filter_params, doseq=True)
    
    context['query_string'] = query_string # Добавляем query_string в контекст
    print(f"[DEBUG] rim_list: Сформирован query_string: '{query_string}'")
    print(f"[DEBUG] rim_list: Количество дисков на текущей странице ({page_obj.number}): {len(page_obj.object_list)} шт.")

    # Если HTMX-запрос — возвращаем только partial
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'tyres/_rims_list.html', context)

    return render(request, 'tyres/rim_list.html', context)

def rim_detail(request, rim_id):
    rim = get_object_or_404(RimModel, id=rim_id)
    variants = rim.variants.all()
    favourite_rim_variant_ids = []
    if request.user.is_authenticated:
        favourite_rim_variant_ids = list(request.user.favourite_rims.filter(rim_variant__in=variants).values_list('rim_variant_id', flat=True))
    
    # Параметры для вариантов дисков
    diameters = sorted(list(set(v.diameter for v in variants)))
    widths = sorted(list(set(v.width for v in variants)))
    bolt_patterns = sorted(list(set(v.bolt_pattern for v in variants)))
    offsets = sorted(list(set(v.offset for v in variants)))
    dias = sorted(list(set(v.dia for v in variants)))
    colors = sorted(list(set(v.color for v in variants)))
    materials = sorted(list(set(v.material for v in variants)))

    context = {
        'rim': rim,
        'variants': variants,
        'diameters': diameters,
        'widths': widths,
        'bolt_patterns': bolt_patterns,
        'offsets': offsets,
        'dias': dias,
        'colors': colors,
        'materials': materials,
        'favourite_rim_variant_ids': favourite_rim_variant_ids,
    }
    return render(request, 'tyres/rim_detail.html', context)

@require_POST
@login_required
def add_favourite_rim(request, variant_id):
    rim_variant = get_object_or_404(RimVariant, id=variant_id)
    FavouriteRim.objects.get_or_create(user=request.user, rim_variant=rim_variant)
    # Возвращаем пустой ответ или часть шаблона, если это HTMX запрос
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'tyres/_rim_variant_row_partial.html', {'variant': rim_variant, 'is_favourited': True})
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
@login_required
def remove_favourite_rim(request, variant_id):
    rim_variant = get_object_or_404(RimVariant, id=variant_id)
    FavouriteRim.objects.filter(user=request.user, rim_variant=rim_variant).delete()
     # Возвращаем пустой ответ или часть шаблона, если это HTMX запрос
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'tyres/_rim_variant_row_partial.html', {'variant': rim_variant, 'is_favourited': False})
    return redirect(request.META.get('HTTP_REFERER', '/'))

@user_passes_test(lambda u: u.is_staff)
def admin_rims(request):
    # Здесь будет логика для администрирования дисков
    pass

@user_passes_test(lambda u: u.is_staff)
def admin_rim_add(request):
    # Здесь будет логика для добавления диска
    pass

@user_passes_test(lambda u: u.is_staff)
def admin_rim_edit(request, rim_id):
    # Здесь будет логика для редактирования диска
    pass

@user_passes_test(lambda u: u.is_staff)
def admin_rim_delete(request, rim_id):
    # Здесь будет логика для удаления диска
    pass
