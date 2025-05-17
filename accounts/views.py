from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from orders.models import Order
from django import forms

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена')
            return redirect('tyres:catalogue')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('tyres:catalogue')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=request.user)
    
    orders = Order.objects.filter(user=request.user).prefetch_related('items__tyre')
    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders
    })

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('tyres:catalogue')

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_panel(request):
    return render(request, 'accounts/admin_panel.html')

@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'accounts/admin_users.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def admin_user_detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/admin_user_detail.html', {'user_obj': user})

@user_passes_test(lambda u: u.is_staff)
def admin_user_edit(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    class UserEditForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
            widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_users')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'accounts/admin_user_edit.html', {'form': form, 'user_obj': user})

@user_passes_test(lambda u: u.is_staff)
def admin_user_delete(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:admin_users')
    return render(request, 'accounts/admin_user_delete.html', {'user_obj': user}) 