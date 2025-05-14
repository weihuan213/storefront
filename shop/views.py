from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {'product': product})

from django.db.models import Q

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, "shop/search.html", {'products': products, 'query': query})

from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def cart_detail(request):
    # 获取或创建未支付的订单
    order, created = Order.objects.get_or_create(
        user=request.user,
        paid=False
    )
    return render(request, "shop/cart_detail.html", {'order': order})

from django.shortcuts import redirect

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(
        user=request.user,
        paid=False
    )
    # 更新或创建 OrderItem
    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'price_at_order': product.price, 'quantity': 1}
    )
    if not item_created:
        item.quantity += 1
        item.save()
    return redirect('shop:cart_detail')


# cart/views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Product

# @login_required
# def cart_remove(request, product_id):
#     """从购物车移除商品"""
#     cart = request.session.get('cart', {})
#
#     if str(product_id) in cart:
#         # 移除单个商品
#         del cart[str(product_id)]
#         request.session['cart'] = cart
#         request.session.modified = True
#         # 可选：添加Django消息框架提示
#         # from django.contrib import messages
#         # messages.success(request, "商品已移除")
#
#     return redirect('cart:cart_detail')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Order, OrderItem


@login_required
def cart_remove(request, pk):
    # 获取要操作的商品
    product = get_object_or_404(Product, pk=pk)

    # 获取用户未支付的订单
    order = get_object_or_404(
        Order,
        user=request.user,
        paid=False
    )

    # 获取对应的订单项
    item = get_object_or_404(
        OrderItem,
        order=order,
        product=product
    )

    # 减少数量或删除
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    # 如果订单没有商品项了，删除空订单（可选）
    if not order.items.exists():
        order.delete()

    return redirect('shop:cart_detail')

@login_required
def checkout(request):
    order = get_object_or_404(Order, user=request.user, paid=False)
    if request.method == 'POST':
        # 处理支付逻辑（此处需集成支付接口）
        order.paid = True
        order.save()
        return redirect('shop:order_success')
    return render(request, "shop/checkout.html", {'order': order})

def order_success(request):
    return render(request, "shop/order_success.html")