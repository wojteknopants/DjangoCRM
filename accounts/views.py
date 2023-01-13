from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    pending_orders = orders.filter(status="Pending").count()
    delivered_orders = orders.filter(status="Delivered").count()

    CONTEXT = {
        "orders" : orders, 
        "customers" : customers,
        "total_orders" : total_orders,
        "pending_orders" : pending_orders,
        "delivered_orders" : delivered_orders,
    }

    return render(request, 'accounts/dashboard.html', CONTEXT)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {"products" : products})

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer_orders = customer.order_set.all()
    total_orders = customer_orders.count()

    orderfilter = OrderFilter(request.GET, queryset = customer_orders)
    customer_orders = orderfilter.qs

    CONTEXT = {
        "customer" : customer,
        "customer_orders" : customer_orders,
        "total_orders" : total_orders,
        "orderfilter" : orderfilter,
    }

    return render(request, 'accounts/customer.html', CONTEXT)

@login_required(login_url='login')
def createOrder(request, pk):

    customer = Customer.objects.get(pk=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status", "note"), extra=1)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    CONTEXT = {
        'formset' : formset,
    }

    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer', pk=customer.pk)

    return render(request, 'accounts/order_form.html', CONTEXT)

@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    CONTEXT = {
        'form' : form,
    }

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_update.html', CONTEXT)

@login_required(login_url='login')
def removeOrder(request, pk):
    order = Order.objects.get(pk=pk)

    CONTEXT = {
        'order' : order,
    }

    if request.method == "POST":
        order.delete()
        return redirect('/')

    return render(request, 'accounts/order_delete.html', CONTEXT)

@login_required(login_url='login')
def createCustomer(request):

    form = CustomerForm()
    CONTEXT = {
        'form' : form,
    }

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/customer_form.html', CONTEXT)

@login_required(login_url='login')
def updateCustomer(request, pk):

    customer = Customer.objects.get(pk=pk)
    form = CustomerForm(instance=customer)

    CONTEXT = {
        'form' : form,
    }

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/customer_form.html', CONTEXT)


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        CONTEXT = {
            'form' : form,
        }

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            print("username is " + request.POST['username'])
            if form.is_valid():
                form.save()
                user = request.POST["username"]
                messages.success(request, "Account was created for " + user)
                return redirect('login')

            else:
                CONTEXT = {'form' : form,}
                return render(request, 'accounts/register.html', CONTEXT)
                

                
        return render(request, 'accounts/register.html', CONTEXT)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('/')
    else:
        
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Credentials are incorrect")


        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')




