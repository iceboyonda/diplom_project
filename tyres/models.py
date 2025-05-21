from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class TyreModel(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    brand = models.CharField('Бренд', max_length=100, db_index=True)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='tyres/', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['brand', 'name']),
        ]
        ordering = ['brand', 'name']

    def __str__(self):
        return f"{self.brand} {self.name}"

class TyreVariant(models.Model):
    SEASON_CHOICES = [
        ('summer', 'Летние'),
        ('winter', 'Зимние'),
        ('all_season', 'Всесезонные'),
    ]
    SPEED_INDEX_CHOICES = [
        ('Q', 'Q (160 км/ч)'),
        ('R', 'R (170 км/ч)'),
        ('S', 'S (180 км/ч)'),
        ('T', 'T (190 км/ч)'),
        ('H', 'H (210 км/ч)'),
        ('V', 'V (240 км/ч)'),
        ('W', 'W (270 км/ч)'),
        ('Y', 'Y (300 км/ч)'),
        ('ZR', 'ZR (>240 км/ч)'),
    ]
    model = models.ForeignKey(TyreModel, related_name='variants', on_delete=models.CASCADE)
    width = models.IntegerField('Ширина', validators=[MinValueValidator(125), MaxValueValidator(445)])
    profile = models.IntegerField('Профиль', validators=[MinValueValidator(25), MaxValueValidator(100)])
    radius = models.IntegerField('Радиус', validators=[MinValueValidator(13), MaxValueValidator(24)])
    season = models.CharField('Сезон', max_length=20, choices=SEASON_CHOICES, db_index=True)
    studded = models.BooleanField('Шипованная', default=False)
    speed_index = models.CharField('Индекс скорости', max_length=4, choices=SPEED_INDEX_CHOICES)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField('Количество на складе', default=0, validators=[MinValueValidator(0)])

    class Meta:
        indexes = [
            models.Index(fields=['width', 'profile', 'radius']),
            models.Index(fields=['season']),
            models.Index(fields=['price']),
        ]
        ordering = ['model__brand', 'model__name', 'width', 'profile', 'radius']

    def __str__(self):
        return f"{self.model} {self.width}/{self.profile} R{self.radius} {self.speed_index}"

    def is_in_stock(self):
        return self.stock > 0

    def can_order(self, quantity):
        return self.stock >= quantity

class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    variant = models.ForeignKey('TyreVariant', on_delete=models.CASCADE, related_name='favourited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'variant')
        indexes = [
            models.Index(fields=['user', 'added_at']),
        ]
        ordering = ['-added_at']

class Category(models.Model):
    CATEGORY_TYPES = [
        ('tyre', 'Шины'),
        ('disk', 'Диски'),
        ('chem', 'Автохимия'),
        ('other', 'Другое'),
    ]
    name = models.CharField('Название', max_length=100, db_index=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    type = models.CharField('Тип', max_length=20, choices=CATEGORY_TYPES, default='other', db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['type', 'name']),
            models.Index(fields=['parent']),
        ]
        ordering = ['type', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/{self.slug}/'

class RimModel(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    brand = models.CharField('Бренд', max_length=100, db_index=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='rims/', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['brand', 'name']),
        ]
        ordering = ['brand', 'name']
        verbose_name = 'Модель диска'
        verbose_name_plural = 'Модели дисков'

    def __str__(self):
        return f"{self.brand} {self.name}"

class RimVariant(models.Model):
    model = models.ForeignKey(RimModel, related_name='variants', on_delete=models.CASCADE)
    diameter = models.FloatField('Диаметр')
    width = models.FloatField('Ширина')
    bolt_pattern = models.CharField('Тип крепления', max_length=50)
    offset = models.CharField('Вылет (ET)', max_length=20, blank=True)
    dia = models.CharField('DIA', max_length=20, blank=True)
    color = models.CharField('Цвет', max_length=50, blank=True)
    material = models.CharField('Материал', max_length=50)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Количество на складе', default=0)
    image = models.ImageField('Изображение', upload_to='rims/variants/', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['diameter', 'width', 'bolt_pattern']),
            models.Index(fields=['price']),
        ]
        ordering = ['model__brand', 'model__name', 'diameter', 'width']
        verbose_name = 'Вариант диска'
        verbose_name_plural = 'Варианты дисков'

    def __str__(self):
        return f"{self.model} {self.diameter}x{self.width} {self.bolt_pattern}"

class FavouriteRim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_rims')
    rim_variant = models.ForeignKey('RimVariant', on_delete=models.CASCADE, related_name='favourited_by_rims')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'rim_variant')
