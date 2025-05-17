from django.db import models
from django.conf import settings
from tyres.models import TyreVariant

class Cart:
    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, tyre, quantity=1, update_quantity=False):
        """
        Добавить товар в корзину или обновить его количество
        """
        tyre_id = str(tyre.id)
        if tyre_id not in self.cart:
            self.cart[tyre_id] = {'quantity': 0, 'price': str(tyre.price)}
        if update_quantity:
            self.cart[tyre_id]['quantity'] = quantity
        else:
            self.cart[tyre_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохранить корзину в сессии
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, tyre):
        """
        Удалить товар из корзины
        """
        tyre_id = str(tyre.id)
        if tyre_id in self.cart:
            del self.cart[tyre_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение товаров из базы данных
        """
        tyre_ids = self.cart.keys()
        tyres = TyreVariant.objects.filter(id__in=tyre_ids)
        for tyre in tyres:
            self.cart[str(tyre.id)]['tyre'] = tyre
            # Всегда обновляем цену из базы
            self.cart[str(tyre.id)]['price'] = float(tyre.price)

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет количества товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет общей стоимости товаров в корзине
        """
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Очистка корзины
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_quantity(self):
        """
        Получить общее количество товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

class CartItem(models.Model):
    tyre = models.ForeignKey(TyreVariant, on_delete=models.CASCADE) 