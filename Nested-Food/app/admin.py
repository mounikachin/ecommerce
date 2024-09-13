from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header='Nested Food || Admin'

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','is_approved','added_on']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class DishAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','discount_price','added_on','updated_on']

@admin.register(Dish_cart)
class DishCartAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','counter','ammount']

@admin.register(Order_history)
class Order_historyAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity','ammount','status',"date"]

admin.site.register(Contact,ContactAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(Dish,DishAdmin)
admin.site.register(Profile)