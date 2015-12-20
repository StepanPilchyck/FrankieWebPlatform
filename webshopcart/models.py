from django.db import models

# WebShop Models
from webshop.models import Product, ProductPriceCorrector

# Chained selects support
from smart_selects.db_fields import ChainedForeignKey


class ProductInCart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product)
    cart = models.ForeignKey('ProductCart')
    count = models.IntegerField()
    price_correction = ChainedForeignKey(
        ProductPriceCorrector,
        chained_field="product",
        chained_model_field="product",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True
    )

    def price(self):
        sale = 1
        if self.product.sale:
            sale = 1 - (self.product.sale.percent / 100)
        margin = 1
        if self.product.margin:
            margin = 1 - (self.product.margin.percent / 100)
        if self.price_correction:
            return self.price_correction.get_new_price * self.count * sale / margin
        return self.product.get_default_price * self.count * sale / margin

    def __str__(self):
        return str.format("{0} ({1}) = {2}",
                          self.product, self.count, self.price())

    class Meta:
        db_table = 'products_in_carts'
        verbose_name = 'Product in Cart'
        verbose_name_plural = 'Products in Carts'


class ProductCart(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    date_on_add = models.DateTimeField(auto_now_add=True)
    date_on_close = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    fixed_sum = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str.format("User: {0} || Email: {1} || Phone: {2} || Description: {3} || Date: {4}",
                          self.username, self.email, self.phone, self.description, self.date_on_add)

    def all_products(self):
        products = ProductInCart.objects.filter(cart=self).all()
        res = ''
        for product in products:
            res += product.__str__() + '</br>'
        return res

    def sum(self):
        products = ProductInCart.objects.filter(cart=self).all()
        res = 0
        for product in products:
            res += product.price()
        return res

    all_products.allow_tags = True

    def check_sum(self):
        if self.fixed_sum ==self.sum():
            return True
        return False

    class Meta:
        db_table = 'product_carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

