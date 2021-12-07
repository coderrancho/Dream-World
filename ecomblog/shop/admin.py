from django.contrib import admin

# Register your models here.

from .models import Product,Contact,Order,orderUpdate,Signup

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(orderUpdate)
admin.site.register(Signup)
