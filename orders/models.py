from django.db import models
from django.contrib.auth.models import User
from tyres.models import TyreVariant, RimVariant

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес доставки', max_length=250)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    city = models.CharField('Город', max_length=100)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    note = models.TextField('Примечание', blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    tyre = models.ForeignKey(TyreVariant, related_name='order_items', on_delete=models.CASCADE, verbose_name='Шина', null=True, blank=True)
    rim = models.ForeignKey(RimVariant, related_name='order_items', on_delete=models.CASCADE, verbose_name='Диск', null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.tyre and not self.rim:
            raise ValidationError('Необходимо указать либо шину, либо диск')
        if self.tyre and self.rim:
            raise ValidationError('Нельзя указать и шину, и диск одновременно') 