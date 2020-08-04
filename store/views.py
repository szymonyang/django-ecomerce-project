import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from store.models import Product, Order, OrderItem, ShippingAddress
from store.utils import cookieCart


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        # items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    print("context:", context)
    return render(request, "store/cart.html", context)


class CartView(View):
    def get(self, request: HttpRequest):
        print(request.COOKIES)
        if request.user.is_authenticated:
            customer = request.user.customer
            # Todo: Should consider a user might have multiple order
            order = Order.objects.get(customer=customer)
            items = order.order_item.all()
        else:
            # Create empty cart for now for non-logged in user
            try:
                cart = json.loads(request.COOKIES["cart"])
            except:
                cart = {}
                print("CART:", cart)

            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0}
            cartItems = order["get_cart_items"]

        context = {"items": items}
        return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    # Todo: should restrict POST only
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # TODO: Dangerous. No exception handling
    # TODO: Handle multiple order
    order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
    # TODO: Dangerous
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    # Should restrict to POST only
    data = json.loads(request.body)
    if request.user.is_authenticated:
        # TODO: Why 1to1 field (maybe the reverese lookup)
        customer = request.user.customer
        # print(request.user.customer)
        # Handle multiple order
        order, _ = Order.objects.get_or_create(customer=customer, is_complete=False)
        total = float(data['form']['total'])
        if total == order.get_cart_total:
            order.complete = True
            order.save()

        ShippingAddress.objects.create(
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )
    else:
        print("User is not logged in")

    return JsonResponse('Payment submitted..', safe=False)
