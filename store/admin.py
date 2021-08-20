from django.contrib import admin
from .models import Customer, OrderDetail, Product,Catagory,Order



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','description','catagory')
    search_fields = ('name','price','catagory')
admin.site.register(Product,ProductAdmin)



class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Catagory,CatagoryAdmin)



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','email','password')
    search_fields = ('first_name','last_name','phone','email')
admin.site.register(Customer,CustomerAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','date',)
    search_fields = ('customer''date',)
admin.site.register(Order,OrderAdmin)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order','product','price','quantity')
    search_fields = ('order','product','price','quantity')
admin.site.register(OrderDetail,OrderDetailAdmin)