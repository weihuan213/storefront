import os
import django
import random
from faker import Faker
from django.utils import timezone

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
django.setup()

from django.contrib.auth import get_user_model
from shop.models import Category, Product, Order, OrderItem

User = get_user_model()
fake = Faker()


def delete_old_data():
    """（可选）清理旧数据"""
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    User.objects.filter(is_staff=False).delete()


def create_users(num=3):
    """创建测试用户"""
    for _ in range(num):
        try:
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            print(f'创建用户: {user.username}')
        except django.db.IntegrityError:
            pass


def create_categories(num=5):
    """创建商品分类"""
    for _ in range(num):
        name = fake.unique.word().capitalize()
        Category.objects.get_or_create(name=name)
    print(f'已创建 {num} 个分类')


def create_products(num_per_category=5):
    """创建商品"""
    categories = Category.objects.all()
    for category in categories:
        for _ in range(num_per_category):
            Product.objects.create(
                sku=f'SKU-{fake.unique.bothify(text="??##").upper()}',
                name=fake.sentence(nb_words=3).replace('.', ''),
                category=category,
                price=fake.pydecimal(left_digits=3, right_digits=2,
                                     min_value=10, max_value=1000),
                description=fake.text(max_nb_chars=200),
                stock=fake.random_int(min=0, max=100),
                image_url=fake.image_url()
            )
    print(f'每分类创建 {num_per_category} 个商品')


def create_orders(num_per_user=2):
    """创建订单"""
    for user in User.objects.all():
        for _ in range(num_per_user):
            order = Order.objects.create(user=user, paid=fake.boolean())
            # 设置历史时间
            order.created = timezone.make_aware(
                fake.date_time_between('-1y', 'now')
            )
            order.save(update_fields=['created'])
    print(f'每用户创建 {num_per_user} 个订单')


def create_order_items():
    """创建订单项"""
    products = list(Product.objects.all())
    for order in Order.objects.all():
        for product in random.sample(products, k=random.randint(1, 5)):
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=random.randint(1, 10),
                price_at_order=product.price
            )
    print('订单项创建完成')


if __name__ == '__main__':
    # 删除旧数据（谨慎使用）
    # delete_old_data()

    create_users(3)
    create_categories(10)
    create_products(3000)
    create_orders(200)
    create_order_items()
    print("测试数据生成完成！")