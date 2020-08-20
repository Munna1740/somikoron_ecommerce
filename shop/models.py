from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from stdimage import StdImageField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

ORDER_STATUS = (
    ('PLACED', 'Order Placed'),
    ('RECEIVED', 'Order Received'),
    ('SHIPPING', 'Order is on the way'),
    ('DONE', 'Order Completed'),
    ('CANCELED', 'Order Canceled'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class OwnerInfo(models.Model):
    owner_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.owner_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_id = models.CharField(max_length=10)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("shop:category-items", kwargs={
            'catid': self.category_id
        })


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.sub_category_name + " (" + self.category.category_name + ")"

    def get_absolute_url(self):
        print(self.pk)
        return reverse("shop:item-list", kwargs={
            'subid': self.pk
        })


class Items(models.Model):
    product_code = models.CharField(max_length=10, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_DEFAULT, default=1)
    # label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    item_owner = models.ForeignKey(OwnerInfo, on_delete=models.SET_NULL, \
                                   null=True, blank=True)

    # image = models.ImageField(u'Images')
    # class Meta:
    #     ordering = ['-update_date']
    def __str__(self):
        return str(self.pk) + " " + self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'slug': self.slug
        })


class ItemDetails(models.Model):
    item = models.OneToOneField(
        Items, on_delete=models.CASCADE, related_name='itemdetails',
    )
    discount_offer = models.FloatField(default=0)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    stock_quantity = models.IntegerField(null=True, blank=True, default=1)
    update_date = models.DateTimeField(auto_now=True)
    total_views = models.IntegerField(default=0)
    additional_info = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.item.title

    class Meta:
        ordering = ['-update_date']

    def get_absolute_url(self):
        return reverse("shop:itemdetails", kwargs={
            'slug': self.slug
        })

    def get_discounted_price(self):
        if self.discount_offer >= 1:
            return self.item.price - self.discount_offer
        else:
            return (self.item.price) - (self.discount_offer * self.item.price)


class CattleInfo(models.Model):
    item = models.OneToOneField(Items, on_delete=models.CASCADE, related_name='cattleinfo')
    height = models.CharField(max_length=15, null=True, blank=True)
    live_weight = models.FloatField(max_length=10, null=True, blank=True)
    expected_weight = models.FloatField(max_length=10, null=True, blank=True)
    Breed = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.item.item_owner.owner_name + "-" + self.item.title


class ItemImages(models.Model):
    item = models.ForeignKey(
        Items, on_delete=models.CASCADE, related_name='images', null=True, blank=True,

    )
    # image = StdImageField(upload_to='media/images/')
    # image1 = StdImageField(upload_to='path/to/img')  # works as ImageField
    # image2 = StdImageField(upload_to='path/to/img', blank=True)  # can be deleted throwgh admin
    # image3 = StdImageField(upload_to='path/to/img', variations={'thumbnail': (100, 75)})  # creates a thumbnail resized to maximum size to fit a
    # 100x75 area
    # image4 = StdImageField(upload_to='path/to/img', variations={'thumbnail': (100, 100, True)})
    image = StdImageField(upload_to='media/images/', blank=True, variations={
        'thumbnail': (220,
                      140)}, delete_orphans=True)  # all previous features in one declaration

    def __str__(self):
        return str(self.item.product_code) + " " + self.item.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.itemdetails.get_discounted_price()

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.itemdetails.discount_offer > 0:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_note = models.TextField(max_length=500, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PLACED')
    payment_method = models.CharField(max_length=12, null=True, blank=True, default='CASH ON')
    payment_status = models.CharField(max_length=12, null=True, blank=True, default='PENDING')
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True,
        null=True)

    def __str__(self):
        return f"{self.user} - {self.ordered}- {self.order_status}"

    # billing_address = models.ForeignKey(
    #     'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True,
    #     null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    # being_delivered = models.BooleanField(default=False)
    # received = models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)
    #
    # '''
    # 1. Item added to cart
    # 2. Adding a billing address
    # (Failed checkout)
    # 3. Payment
    # (Preprocessing, processing, packaging etc.)
    # 4. Being delivered
    # 5. Received
    # 6. Refunds
    # '''
    # def __str__(self):
    #     return self.user.username
    #
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=20)
    customer_phone = models.CharField(max_length=15)
    area = models.CharField(max_length=30)
    address = models.CharField(max_length=200)

    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class MonthlyPackage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_list = models.TextField(max_length=700)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PLACED')
    payment_method = models.CharField(max_length=12, null=True, blank=True, default='CASH ON')
    payment_status = models.CharField(max_length=12, null=True, blank=True, default='PENDING')
    shipping_address = models.ForeignKey(
        'Address', related_name='monthly_shipping_address', on_delete=models.SET_NULL, blank=True,
        null=True)

    def __str__(self):
        return f"{self.user} - {self.order_status}"
