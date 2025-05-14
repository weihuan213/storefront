# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'  # 与项目级 include 中的 namespace 对应

urlpatterns = [
    # 商品列表
    path('', views.product_list, name='product_list'),

    # 商品详情：/shop/123/
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # 搜索：/shop/search/?q=xxx
    path('search/', views.search, name='search'),

    # 购物车查看：/shop/cart/
    path('cart/', views.cart_detail, name='cart_detail'),

    # 加入购物车：/shop/cart/add/123/
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),

    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    # 结算／下单：/shop/checkout/
    path('checkout/', views.checkout, name='checkout'),

    # 订单成功页：/shop/order/success/
    path('order/success/', views.order_success, name='order_success'),

]
