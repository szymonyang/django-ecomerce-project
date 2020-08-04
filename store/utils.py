import json

from django.core.exceptions import ObjectDoesNotExist

from store.models import Product


def cookieCart(request):
    try:
        cart_from_cookie = json.loads(request.COOKIES["cart"])
    except KeyError:
        cart_from_cookie = {}
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0}
    cartItems = order["get_cart_items"]
    for i in cart_from_cookie:
        try:
            cartItems += cart_from_cookie[i]['quantity']
            product = Product.objects.get(id=i)

            total = (product.price * cart_from_cookie[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart_from_cookie[i]['quantity']

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'imageURL': product.image_url}, 'quantity': cart_from_cookie[i]['quantity'],
                'digital': product.is_digital, 'get_total': total,
            }
            items.append(item)
        except ObjectDoesNotExist:
            print(f"item id: {i} does not exist.")
            pass
    context = {"items": items, "order": order, "cartItems": cartItems}
    return context
