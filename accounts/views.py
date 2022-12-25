from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

from .models import *
from .forms import OrderForm, CustomerForm

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

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {"products" : products})

def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer_orders = customer.order_set.all()
    total_orders = customer_orders.count()

    CONTEXT = {
        "customer" : customer,
        "customer_orders" : customer_orders,
        "total_orders" : total_orders
    }

    return render(request, 'accounts/customer.html', CONTEXT)

def createOrder(request):

    form = OrderForm()
    CONTEXT = {
        'form' : form,
    }

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', CONTEXT)


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

    return render(request, 'accounts/order_form.html', CONTEXT)

def removeOrder(request, pk):
    order = Order.objects.get(pk=pk)

    CONTEXT = {
        'order' : order,
    }

    if request.method == "POST":
        order.delete()
        return redirect('/')

    return render(request, 'accounts/order_delete.html', CONTEXT)


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




