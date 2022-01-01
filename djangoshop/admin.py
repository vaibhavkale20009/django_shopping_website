from django.contrib import admin
from django.db.models import fields
from djangoshop.models import items
from djangoshop.models import cartdb

# Register your models here.

class itemsadmin(admin.ModelAdmin):
    field_list=['name','desc','price','category','stock','disc','img','offers']
admin.site.register(items,itemsadmin)

class checkoutadmin(admin.ModelAdmin):
    field_list=['name','price','img','username']
admin.site.register(cartdb,checkoutadmin)
