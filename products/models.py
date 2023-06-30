from django.db import models
from django.contrib.auth.models import User



# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def authenticate(self, password):
        return self.password == password
    
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class AddProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    quantity=models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/img/')

class CartItem(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE, related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
    
class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('User', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('AddProduct',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    
    
    