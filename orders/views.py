from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.models import Cart

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    tyre=item['tyre'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Очищаем корзину
            cart.clear()
            messages.success(request, 'Заказ успешно оформлен')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # Предзаполняем форму данными пользователя
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = request.user.orders.get(id=order_id)
    return render(request, 'orders/detail.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):
    orders = Order.objects.all().select_related('user')
    return render(request, 'orders/admin_orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user'), id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != order.status:
            order.status = new_status
            order.save()
    return render(request, 'orders/admin_order_detail.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user'), id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:admin_orders')
    return render(request, 'orders/admin_order_delete.html', {'order': order}) 