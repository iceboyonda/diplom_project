from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db.models.functions import Lower
from .models import TyreModel, TyreVariant, Favourite
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from urllib.parse import urlencode
from .forms import TyreModelForm, TyreVariantFormSet

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

def catalogue(request):
    tyres = TyreModel.objects.prefetch_related('variants').all()
    paginator = Paginator(tyres, 6)  # 6 шин на страницу (2 в ряд, 3 ряда)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    annotate_tyres(page_obj.object_list)
    brands = TyreModel.objects.values_list('brand', flat=True)
    brands = sorted(set(b.strip().capitalize() for b in brands if b))
    widths = sorted(set(TyreVariant.objects.values_list('width', flat=True)))
    profiles = sorted(set(TyreVariant.objects.values_list('profile', flat=True)))
    radiuses = sorted(set(TyreVariant.objects.values_list('radius', flat=True)))
    context = {
        'page_obj': page_obj,
        'tyres': page_obj.object_list,
        'brands': brands,
        'widths': widths,
        'profiles': profiles,
        'radiuses': radiuses,
        'seasons': dict(TyreVariant.SEASON_CHOICES),
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

def filter_tyres(request):
    tyres = TyreModel.objects.all()
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
    tyres = tyres.distinct()
    # Пагинация
    page_number = request.GET.get('page')
    paginator = Paginator(tyres, 6)
    page_obj = paginator.get_page(page_number)
    annotate_tyres(page_obj.object_list)
    # Собираем query_string для фильтров (кроме page)
    filter_params = request.GET.copy()
    if 'page' in filter_params:
        filter_params.pop('page')
    query_string = ''
    if filter_params:
        query_string = '&' + urlencode(filter_params, doseq=True)
    # Для HTMX-запроса возвращаем partial (список + пагинация)
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'tyres/_tyres_list.html', {
            'tyres': page_obj.object_list,
            'page_obj': page_obj,
            'query_string': query_string
        })
    # Для обычного запроса возвращаем всю страницу
    brands = TyreModel.objects.values_list('brand', flat=True)
    brands = sorted(set(b.strip().capitalize() for b in brands if b))
    widths = sorted(set(TyreVariant.objects.values_list('width', flat=True)))
    profiles = sorted(set(TyreVariant.objects.values_list('profile', flat=True)))
    radiuses = sorted(set(TyreVariant.objects.values_list('radius', flat=True)))
    context = {
        'page_obj': page_obj,
        'tyres': page_obj.object_list,
        'brands': brands,
        'widths': widths,
        'profiles': profiles,
        'radiuses': radiuses,
        'seasons': dict(TyreVariant.SEASON_CHOICES),
        'query_string': query_string,
    }
    return render(request, 'tyres/catalogue.html', context)

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
    
    annotate_tyres(tyres)
    
    return render(request, 'tyres/catalogue.html', {'tyres': tyres, 'query': query})

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
    favourite_variants = TyreVariant.objects.filter(favourited_by__user=request.user).select_related('model')
    return render(request, 'tyres/favourites.html', {'favourite_variants': favourite_variants})

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
