from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Table'

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(upload_to="categories")
    icon = models.CharField(max_length=60,blank=True)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # facebook_url = models.URLField(blank=True)
    # twitter_url = models.URLField(blank=True())
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Team Table'

class Dish(models.Model):
    name = models.CharField(max_length=200,unique=True)
    image = models.ImageField(upload_to="dishes")
    ingredients = models.TextField()
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    price = models.FloatField()
    discount_price = models.FloatField(blank=True)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Dish Table'

class Dish_cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.ForeignKey(Dish,on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    ammount = models.PositiveBigIntegerField(null=True)
    def __str__(self):
        return self.name.name

class Order_history(models.Model):
    order_status = [('Pending','Pending'),('Packed','Packed'),('Delivered','Delivered'),('Cancel','Cancel')]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Dish,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ammount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=200,choices=order_status,default='Pending')
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.user.first_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profiles", null=True,blank=True)
    address = models.TextField(blank=True)
    contact = models.IntegerField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = 'Profile Table'


        