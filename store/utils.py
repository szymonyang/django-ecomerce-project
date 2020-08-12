import json

from django.core.exceptions import ObjectDoesNotExist

from store.models import Product, Order, Customer, OrderItem


def cookieCart(request):
    try:
        cart_from_cookie = json.loads(request.COOKIES["cart"])
    except KeyError:
        cart_from_cookie = {}

    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cartItems = 0

    for i in cart_from_cookie.keys():
        try:
            cartItems += cart_from_cookie[i]["quantity"]
            product = Product.objects.get(id=i)

            total = (product.price * cart_from_cookie[i]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart_from_cookie[i]["quantity"]

            item = {
                "id": product.id,
                "product": {"id": product.id, "name": product.name, "price": product.price,
                            "imageURL": product.image_url}, "quantity": cart_from_cookie[i]["quantity"],
                "digital": product.is_digital, "get_total": total,
            }
            items.append(item)
        except ObjectDoesNotExist:
            print(f"item id: {i} does not exist.")
            pass
    context = {"items": items, "order": order, "cartItems": cartItems}
    return context


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return {"cartItems": cartItems, "order": order, "items": items}


def guestOrder(request, data) -> (Customer, Order):
    first_name = data["form"]["first_name"]
    last_name = data["form"]["last_name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, _ = Customer.objects.get_or_create(
        email=email,
    )
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        is_complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item["id"])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item["quantity"],
        )
    return customer, order
