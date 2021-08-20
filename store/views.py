from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from .models import Catagory, OrderDetail, Product,Customer,Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def validated_username(request):
    if request.POST:
        data = json.loads(request.body)
        email = data['email']
        print(type(email))
        if  not email.isalnum():
             return JsonResponse({'username_valid':'username must be of alphanumric character'})
        try:
            a1 = Customer.objects.get(email=email)
            if a1:
                return JsonResponse({'username_valid':'username already exist'})
        except Exception as e:
            return JsonResponse({'username_valid':"Username Availaible"},status=200)

    return JsonResponse({'username_valid':"Username Availaible"},status=200)




class Index(View):
    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        products = None
        user = request.session.get('user')
        category = request.GET.get('category')
        print(category )
        if category:
            products = Product.getAllproductsByCategoryId(category)
        else:
            products = Product.getAllproducts()
        catagories = Catagory.getAllcatagories()
        context={ 'products':products,'catagories':catagories,'user':user} 
        return render(request,"store/index.html",context)
    
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        if remove:
            print(remove)
        print(product)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:   
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                 cart[product] = 1

        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(cart)
            
        return redirect('index')
        pass



class CartView(View):
    def get(self,request):
        ids = list( request.session.get('cart').keys())
        products = Product.products_by_id(ids)
        print(products)
        context={'products':products}
        return render(request,"store/cart.html",context)
    

class LoginView(View):
    return_url = None
    def get(self,request):
        LoginView.return_url = request.GET.get('return_url')
        return render(request,"store/login.html",)
    
    def post(sself,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)
        error_message = None
        customer = Customer.get_customer_by_email(email)  
        if customer:
            flag =  check_password (password,customer.password)
            if flag:
                request.session['user'] = customer.first_name
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                request.session['firstname'] = customer.first_name
                request.session['lastname'] = customer.last_name

                if LoginView.return_url:
                    return response.HttpResponseRedirect(LoginView.return_url)
                else: 
                    LoginView.return_url=None
                    return redirect('index')
            else:
                error_message="Please enter valid Email/Password"
        else:
            error_message="Please enter valid Email/Password"
        return render(request,"store/login.html",{'error':error_message})

class SignUpView(View):
    def get(self,request):
        return render(request,"store/signup.html",)

    def post(self,request):
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        phone= request.POST.get('mob_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        
        error_message = None
        customer = Customer.objects.filter(email=email).count()
        
        
        
        if customer > 0:
            error_message = "User with this email already exist" 
        if password != password1:
            error_message =  "Password and confirm password doesn't match"

        
        
        
        if error_message is None:
            c1 = Customer.objects.create(first_name = first_name,last_name=last_name,phone=phone,email=email,password=make_password(password))
            c1.save()
            return redirect('index')
        else:
            value = {
                'first_name':first_name,
                'last_name':last_name,
                'phone':phone,
                'email':email
        }
            data = {

                'error':error_message,
                'values':value
            }
            return render(request,"store/signup.html",data)

def logout(request):
    request.session.clear()
    return redirect('index')

class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        customer = request.session.get('customer_id') 
        o1 = Order.objects.create(customer= Customer(id=customer),address=address,)
        o1.save()
        cart = request.session.get('cart')
        products = Product.products_by_id(list(cart.keys()))
        for product in products:
            od1 = OrderDetail.objects.create(order= o1,product=product,quantity=cart.get(str(product.id)),price=product.price)
            od1.save()
        request.session['cart'] = {}
        print( request.session['cart'])
        return redirect('cart')


class OrderView(View):
    def get(self,request):
        orders = Order.objects.filter(customer=Customer(id = request.session.get('customer_id'))).order_by('-date')
        order_detail = OrderDetail.objects.all()
        print(order_detail)
        context={
            'orders':orders,
            'order_detail':order_detail,
        }
        return render(request,"store/order.html",context)



#Decorator
def auth_middleware(get_response):
    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        if not request.session.get('user'):
            return redirect(f'login?return_url={returnUrl}')  
        response = get_response(request)
        return response
    return middleware