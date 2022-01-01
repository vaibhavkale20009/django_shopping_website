from django import forms
from django.shortcuts import render,redirect
from djangoshop import models
from djangoshop.models import items
from djangoshop.models import cartdb
from djangoshop import forms
from djangoshop.models import cartdb
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from djangoshop import signupform
from django.db.models import Sum
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.

@login_required
def product_view(request):
    products=items.objects.all()
    return render(request,'djangoshop/products.html',{'products':products})
@login_required
def add_product_view(request):
    form=forms.itemform()
    if(request.method=='POST'):
        form=forms.itemform(request.POST,request.FILES)
        if(form.is_valid()):
            print('form valid')
            form.save(commit=True)
            return render(request,'djangoshop/products.html')
    return render(request,'djangoshop/addproduct.html',{'form':form})

@login_required(login_url='/products/')
def checkout_view(request,pk):
        obj=items.objects.get(pk=pk)
        nm= obj.name
        im=  obj.img
        pr=obj.price
        user=request.user
        cart= cartdb(name=nm,img=im,price=pr,username=user)
        cart.save()
        allobj = cartdb.objects.all().filter(username=user)
        total_prices = sum(product.price for product in allobj)
        return render(request,'djangoshop/checkout.html',{'allobj':allobj,'total_prices':total_prices})

    
@login_required
def checkout(request):
    obj=cartdb.objects.all().filter(username=request.user)
    total_prices = sum(product.price for product in obj)
    return render(request,'djangoshop/checkout1.html',{'obj':obj,'total_prices':total_prices})


def signup_view(request):
    form=signupform.signup()
    if(request.method =='POST'):
            form=signupform.signup(request.POST)
            if(form.is_valid()):
                user=form.save()
                user.set_password(user.password)
                user.save()
                print('saved')
                redirect('/products')
    return render(request,'djangoshop/signupform.html',{'form':form})

def del_checkout(request,id):
    cartdb.objects.filter(id=id).delete()
    return render(request,'djangoshop/delete.html')

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def homepage(request):
    currency = 'INR'
    obj=cartdb.objects.all().filter(username=request.user)
    total_prices = sum(product.price for product in obj)
    amount = total_prices*100
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'djangoshop/payments.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                obj=cartdb.objects.all().filter(username=request.user)
                total_prices = sum(product.price for product in obj)
                amount = total_prices*100
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()




