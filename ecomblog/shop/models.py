from django.db import models
from django.utils.timezone import now
# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category=models.CharField(max_length=50,default='')
    subcategory=models.CharField(max_length=50,default='')
    price=models.IntegerField(default=0)
    desc = models.CharField(max_length=400)
    pub_date = models.DateField()
    image=models.ImageField(upload_to='shop/images',default='')

    def __str__(self):
        return self.product_name



class Contact(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email=models.CharField(max_length=50,default='')
    phone=models.CharField(max_length=50,default='')
    desc=models.CharField(max_length=500,default='')

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='')
    address1=models.CharField(max_length=100,default='')
    address2=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    phone=models.CharField(max_length=50,default='')
    zip_code=models.CharField(max_length=500,default='')
    password=models.CharField(max_length=50,default="")

    def __str__(self):
        return self.name

class orderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default='')
    update_desc=models.CharField(max_length=500,default='')
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.update_desc[0:7]+"..."


class Signup(models.Model):
    firstname=models.CharField(max_length=500,default='')
    lastname=models.CharField(max_length=500,default='')
    email=models.CharField(max_length=500,default='')
    city=models.CharField(max_length=500,default='')
    zipcode=models.CharField(max_length=500,default='')
    password=models.CharField(primary_key=True,max_length=100)


    def __str__(self):
        return self.email

