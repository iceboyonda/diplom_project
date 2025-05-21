from django.db import models
from django.conf import settings
from tyres.models import TyreVariant, RimVariant

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

    def add(self, tyre=None, rim=None, quantity=1, update_quantity=False):
        """
        Добавить товар в корзину или обновить его количество
        """
        if tyre:
            product_id = str(tyre.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(tyre.price), 'type': 'tyre'}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()
        elif rim:
            product_id = str(rim.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(rim.price), 'type': 'rim'}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        """
        Сохранить корзину в сессии
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, tyre=None, rim=None):
        """
        Удалить товар из корзины
        """
        if tyre:
            product_id = str(tyre.id)
        elif rim:
            product_id = str(rim.id)
        else:
            return

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение товаров из базы данных
        """
        tyre_ids = [int(k) for k, v in self.cart.items() if v['type'] == 'tyre']
        rim_ids = [int(k) for k, v in self.cart.items() if v['type'] == 'rim']
        tyres = {tyre.id: tyre for tyre in TyreVariant.objects.filter(id__in=tyre_ids)}
        rims = {rim.id: rim for rim in RimVariant.objects.filter(id__in=rim_ids)}
        for product_id, item in self.cart.items():
            if item['type'] == 'tyre':
                item['product'] = tyres.get(int(product_id))
            elif item['type'] == 'rim':
                item['product'] = rims.get(int(product_id))
            item['total_price'] = float(item['price']) * item['quantity']
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