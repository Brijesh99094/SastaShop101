from django import template

register = template.Library()



@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    print(product,cart)
    return False



@register.filter(name='cart_qty')
def cart_qty(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    print(product,cart)
    return False

@register.filter(name='currency')
def currency(number):
    return "₹"+str(number)


@register.filter(name='price_total')
def price_total(product,cart):
    return product.price * cart_qty(product,cart)
   

@register.filter(name='cart_total_price')
def cart_total_price(product,cart):
    t1 = 0
    for prod in product:
        t1+=price_total(prod,cart)
    return t1
