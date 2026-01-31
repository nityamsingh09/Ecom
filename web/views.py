from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse ,JsonResponse
from django.db.models import Avg, Count
from taggit.models import Tag   
from userauth.models import Profile
from web.models import Category, Vendor, Product, ProductImages, ProductReview, CartOrder, CartOrderItems, Wishlist, Address
from userauth.models import ContactUs
from web.forms import ProductReviewForm
from django.template.loader import render_to_string
from .utils import generate_invoice_pdf
import calendar
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear






# Create your views here.

def index(request):
   # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(product_status="published",featured=True).order_by('-id')

    context ={
        'products': products,
    }

    return render(request,'web/index.html',context)


    if request.user.is_authenticated:
        return redirect('web:index')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, 'Invalid login credentials')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('web:index')
        else:
            messages.warning(request, 'Invalid login credentials')

    context ={

    }
    return render(request, 'userauth/sign-in.html',context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by('-id')
    context ={
        'products': products,
    }
    return render(request,'web/product-list.html',context)

def category_list_view(request):
    categories = Category.objects.all()
    context ={
        
        'categories': categories,
    }
    return render(request,'web/category_list_view.html',context)

def category_product_list_view(request,cid):
    category =Category.objects.get(cid=cid)
    products =Product.objects.filter(product_status="published",category=category)

    context ={
        "category": category,
        "products":products,
    }

    return render(request,'web/category-product-list.html',context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context ={
        
        'vendors': vendors,
    }
    return render(request,'web/vendor-list.html',context)


def vendor_detail_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor,product_status="published")
    context ={
        "vendor":vendor,
        "products":products,
    }
    return render(request,"web/vendor-detail.html",context)

from math import floor
from django.db.models import Avg, Count

from math import floor
from django.db.models import Avg, Count

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category=product.category)

    # ⭐ ONLY valid ratings
    reviews = ProductReview.objects.filter(
        product=product,
        rating__isnull=False
    ).order_by("-date")

    # ⭐ Average rating
    avg_rating = reviews.aggregate(rating=Avg("rating"))["rating"] or 0

    avg_full = int(floor(avg_rating))
    avg_has_half = (avg_rating - avg_full) >= 0.5

    review_form = ProductReviewForm()

    # ⭐ Rating counts
    rating_map = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    rating_counts = (
        reviews.values("rating")
        .annotate(count=Count("id"))
        .order_by("-rating")
    )

    for row in rating_counts:
        rating_map[int(row["rating"])] = row["count"]

    total_reviews = reviews.count()

    # ⭐ Percentages
    rating_breakdown = []
    for star in range(5, 0, -1):
        percent = round(
            (rating_map[star] / total_reviews) * 100, 2
        ) if total_reviews > 0 else 0

        rating_breakdown.append({
            "star": star,
            "count": rating_map[star],
            "percent": percent,
        })

    context = {
        "p": product,
        "p_image": p_image,
        "products": products,
        "review_form": review_form,
        "reviews": reviews,
        "average_rating": avg_rating,
        "avg_full": avg_full,
        "avg_has_half": avg_has_half,
        "rating_breakdown": rating_breakdown,
        "total_reviews": total_reviews,
    }

    return render(request, "web/product-detail.html", context)







def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        'products': products,
        'tag': tag,
        
    }
    return render(request, 'web/tag.html', context)




@login_required
def ajax_add_review(request, pid):

    if request.method != "POST":
        return JsonResponse({"bool": False, "error": "Invalid request"})

    product = get_object_or_404(Product, pk=pid)
    user = request.user

    review_text = request.POST.get("review")
    rating = request.POST.get("rating")

    # 🔴 Validation
    if not rating:
        return JsonResponse({
            "bool": False,
            "error": "Rating is required"
        })

    try:
        rating = int(rating)
    except ValueError:
        return JsonResponse({
            "bool": False,
            "error": "Invalid rating"
        })

    # ✅ ONE USER = ONE REVIEW (IMPORTANT FIX)
    review, created = ProductReview.objects.update_or_create(
        user=user,
        product=product,
        defaults={
            "review": review_text,
            "rating": rating,
        }
    )

    context = {
        "user": user.username,
        "review": review.review,
        "rating": review.rating,
        "date": review.date.strftime("%d %b %Y"),
    }

    average_reviews = ProductReview.objects.filter(
        product=product,
        rating__isnull=False
    ).aggregate(avg_rating=Avg("rating"))

    return JsonResponse({
        "bool": True,
        "created": created,   # 👈 NEW
        "context": context,
        "average_reviews": average_reviews,
    })




def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains=query).order_by('date')

    context ={
        'products': products,
        'query': query,
    }

    return render(request, 'web/search.html', context)


def add_to_cart(request):
    cart_product={}
    cart_product[str(request.GET['id'])]={
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
        'size':request.GET['size'],
        'color':request.GET['color'],
        
        
    
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty']) 
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj'])})


            

def cart_view(request):
    cart_total_amount = 0
    
    if 'cart_data_obj' in request.session:
        cart_items = request.session['cart_data_obj']

        for p_id, item in cart_items.items():
            item_total = int(item['qty']) * float(item['price'])   # total per item
            item['item_total'] = item_total                       # add it to the item dict
            cart_total_amount += item_total

        return render(request, 'web/cart.html', {
            "cart_data": cart_items,
            "totalcartitems": len(cart_items),
            "cart_total_amount": cart_total_amount
        })

    else:
        messages.info(request, 'Your cart is empty. Please add some products to your cart.')
        return redirect('web:index')

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
       
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    context =render_to_string("web/async/cart-list.html",{
            "cart_data": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount
        })
    return JsonResponse({"data": context,'totalcartsitems':len(request.session['cart_data_obj'])})  



def checkout_view(request):

    cart_data = {}
    cart_total_amount = 0

    if request.method == "POST":
        request.session["checkout_address"] = {
        "full_name": request.POST.get("full_name") + " " + request.POST.get("last_name"),
        "address": request.POST.get("address"),
        "city": request.POST.get("city"),
        "state": request.POST.get("state"),
        "zip_code": request.POST.get("zip_code"),
        "mobile": request.POST.get("mobile"),
    }
    request.session.modified = True

    


    # 🔹 Case 1: BUY NOW
    if "buy_now" in request.session:
        cart_data = request.session["buy_now"]
        
        
        request.session.modified = True

    # 🔹 Case 2: NORMAL CART
    elif "cart_data_obj" in request.session:
        cart_data = request.session["cart_data_obj"]

    # ❌ dono empty
    if not cart_data:
        messages.warning(request, "Your cart is empty")
        return redirect("web:cart")

    # 💰 Total calculation
    for p_id, item in cart_data.items():
        cart_total_amount += int(item["qty"]) * float(item["price"])
    try:
        active_address = Address.objects.get(user=request.user, status=True)

    except:
        messages.warning(request, "Please add a default address before checkout")
        active_address = None
    return render(
        request,
        "web/checkout.html",
        {
            "cart_data": cart_data,
            "totalcartitems": len(cart_data),
            "cart_total_amount": cart_total_amount,
            "active_address":active_address,
            
        },

    

        
    )

    

from django.http import JsonResponse
from .models import Product

def buy_now(request):
    if request.method == "POST":

        if "cart_data_obj" in request.session:
           del request.session["cart_data_obj"]

        pid = request.POST.get("pid")
        size = request.POST.get("size")
        color = request.POST.get("color")
        qty = int(request.POST.get("qty", 1))
        image = request.POST.get("image")

        product = Product.objects.get(pid=pid)

        # BUY NOW cart (separate from normal cart)
        request.session["buy_now"] = {
            str(product.id): {
                "pid": product.pid,
                "title": product.title,
                "price": str(product.price),
                "image": image,
                "qty": qty,
                "size": size,
                "color": color,
            }
        }
        

        request.session.modified = True

        return JsonResponse({"status": "success"})
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import razorpay
from django.conf import settings


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request):

        payment_method = request.POST.get("payment_method")

        cart_data = request.session.get("buy_now") or request.session.get("cart_data_obj")

        if not cart_data:
            return JsonResponse({"error": "Cart empty"}, status=400)

        subtotal = 0
        for item in cart_data.values():
            subtotal += int(item["qty"]) * float(item["price"])

        shipping_charge = 0

        # 🔴 COD CONDITION
        if payment_method == "COD" and subtotal < 499:
            shipping_charge = 49

        total_amount = subtotal + shipping_charge

        # 🧾 SHIPPING DETAILS (from form)
        full_name = request.POST.get("first_name", "") + " " + request.POST.get("last_name", "")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        mobile = request.POST.get("mobile")

        # 🧾 CREATE ORDER
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
            payment_method=payment_method,
            paid_status=(payment_method == "ONLINE"),
            full_name=full_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            mobile=mobile,
        )

        # 🧾 ITEMS
        for item in cart_data.values():
            CartOrderItems.objects.create(
                order=order,
                user=request.user,
                item=item["title"],
                image=item["image"],
                qty=item["qty"],
                price=item["price"],
                total=float(item["price"]) * int(item["qty"]),
                size=item.get("size", ""),
                color=item.get("color", ""),
            )

        


        # 🟢 COD RESPONSE
        if payment_method == "COD":
            request.session["checkout_order_id"] = order.id
            request.session.modified = True
            return JsonResponse({
                "status": "success",
                "order_id": order.invoice_no
            })


        # 🟢 ONLINE PAYMENT RESPONSE
        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order["amount"],
            "order_id": razorpay_order["id"]
        })





from django.shortcuts import render


@login_required
def payment_success(request):
    razorpay_order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")

    if not payment_id:
        return redirect("web:dashboard")

    payment = client.payment.fetch(payment_id)

    amount = payment["amount"] / 100
    payment_method = payment["method"]

    order = CartOrder.objects.get(
        razorpay_order_id=razorpay_order_id,
        user=request.user
    )

    order.paid_status = True
    order.price = amount
    order.payment_method = payment_method
    order.save()

    # ❌ session.flush() मत करो
    request.session.pop("buy_now", None)
    request.session.pop("cart_data_obj", None)
    request.session.pop("checkout_address", None)

    return render(request, "web/payment_success.html", {
        "order": order,   # 🔥 पूरा order भेजा
    })







@login_required
def payment_success_cod(request):
    order_id = request.session.get("checkout_order_id")

    if not order_id:
        messages.error(request, "Order not found")
        return redirect("web:payment-success-cod")

    order = CartOrder.objects.get(id=order_id, user=request.user)

    # ✅ clear session
    request.session.pop("buy_now", None)
    request.session.pop("cart_data_obj", None)
    request.session.pop("checkout_order_id", None)

    return render(request, "web/payment_success_cod.html", {
        "order_id": order.invoice_no,
        "amount": order.price,
    })




@login_required
def payment_failed(request):
    order_id = request.GET.get("order_id")

    return render(request, "web/payment_failed.html", {
        "order_id": order_id
    })


@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(
        CartOrder,
        invoice_no=order_id,
        user=request.user
    )
    return generate_invoice_pdf(order)



@login_required
def customer_dashboard(request):
    orders_list= CartOrder.objects.filter(user=request.user).order_by('-order_date')
    address = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    

    orders = (
    CartOrder.objects.filter(user=request.user)
    .annotate(month=ExtractMonth('order_date'))
    .values('month')                  # 👈 GROUP BY yahan hota hai
    .annotate(count=Count('id'))
    .values('month', 'count')
)
    month =[]
    total_orders =[]
    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    if request.method == 'POST':
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        new_address= Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, 'Address added successfully')
        return redirect('web:dashboard')


    try:
        mobile_address = Address.objects.get(user=request.user, status=True)

    except:
        messages.warning(request, "Please add a default address before checkout")
        mobile_address = None
    context ={
        'profile': profile,
        'orders_list': orders_list,
        'address': address,
        'orders': orders,
        'mobile_address': mobile_address,
        'month': month,
        'total_orders': total_orders,
        
    }
    return render(request, 'web/dashboard.html',context)

def order_detail_view(request, id):
    orders_list = CartOrder.objects.get(user=request.user,id=id) 
    order_itmes = CartOrderItems.objects.filter(order=orders_list).order_by('-id')
    context ={
        'orders_list': orders_list,
        'order_itmes': order_itmes,
    }
    return render(request, 'web/order-detail.html',context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean':True})

def contact(request):
    
    return render(request,'web/contact.html')


def ajax_contact_form(request):
    full_name = request.GET.get('full_name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    subject = request.GET.get('subject')
    message = request.GET.get('message')

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data ={
        'bool': True,
        'message': "Message sent successfully",
    }
    return JsonResponse({"data" : data})




