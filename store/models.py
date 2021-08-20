from django.db import models
import datetime

from django.db.models.base import Model
# Create your models here.



class Catagory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    
    @staticmethod
    def getAllcatagories():
        return Catagory.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='uploads/products/')
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name

    @staticmethod
    def products_by_id(ids):
        return Product.objects.filter(id__in=ids)


    @staticmethod
    def getAllproducts():
        return Product.objects.all()

    @staticmethod
    def getAllproductsByCategoryId(catagory_id):
        if catagory_id:
            return Product.objects.filter(catagory=catagory_id)
        else:
            Product.getAllproducts()

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)


    def __str__(self):
        return self.first_name
        
    @staticmethod
    def get_customer_by_email(email):
        try:

            return Customer.objects.get(email=email)
        except:
            return False

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address = models.CharField(max_length=50,default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()



