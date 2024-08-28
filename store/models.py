from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('kids', 'Kids'),
        ('accessory', 'accessory'),
        ('phones', 'phones'),
        ('home-office', 'home-office'),
        ('supermarket', 'supermarket'),
        ('appliances', 'appliances'),
        ('games', 'games'),
        ('computer', 'computer'),
        ('health', 'health'),
]
       
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(upload_to='image')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=20)
    
class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1) 
    status = models.BooleanField(default=False) 
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.firstname} {self.customer.lastname}'

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'
    
    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.cartitem_set.all())
        return total_price

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f'{self.product.name} (x{self.quantity})'
    
#     def get_total_price(self):
#         return self.quantity * self.product.price
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.product.price * self.quantity    