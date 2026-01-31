from django.db import models
from shortuuid import uuid
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
import uuid




STATUS_CHOICES = [
    ('rejcted', 'Rejected'),
    ('processing', 'Prosessing'), 
    ('in_transt', 'In Transit'),
    ('out_for_delivery', 'Out for Delivery'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
]
STATUS = [
    ('draft', 'Draft'), 
    ('disabled', 'Disabled'),
    ('rejcted', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
]
RATING = [
    (1, '★☆☆☆☆'), 
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
]

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="cat",alphabet="abcdefghijklmnopqrstuvwxyz0123456789")
    title = models.CharField(max_length=100,default="Shoes")
    image=models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__(self):
        return self.title
    

class Tags(models.Model):
    pass
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="ven",alphabet="abcdefghijklmnopqrstuvwxyz0123456789")
    title = models.CharField(max_length=100)
    image=models.ImageField(upload_to=user_directory_path)
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    address = models.CharField(max_length=100,default="123, Main Street, City, Country")
    chat_response_time = models.CharField(max_length=100,default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    authentic_rating = models.CharField(max_length=100,default="100")
    days_return = models.CharField(max_length=100,default="100")
    warranty_period = models.CharField(max_length=100,default="100")
    contact = models.CharField(max_length=15, default="+91 1234567890")  
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image))
    
    def __str__(self):
        return self.title


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name



class Product(models.Model):
    pid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="pro",alphabet="abcdefghijklmnopqrstuvwxyz0123456789")
    #sizes = models.CharField(max_length=50, default="40")
    sizes = models.ManyToManyField(Size, related_name="products")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True,related_name="category" )
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL, null=True, related_name="product" )
    title = models.CharField(max_length=100,default="Sample Product")
    image=models.ImageField(upload_to=user_directory_path)
    color = models.CharField(max_length=50, default="Default")

    material = models.CharField(max_length=100,default="Cotton")
    description = RichTextUploadingField(null=True, blank=True, default="No description available.")
    


    price = models.DecimalField(max_digits=99999999, decimal_places=2, default=199)
    old_price = models.DecimalField(max_digits=9999999, decimal_places=2, default=299)

    specifications = RichTextUploadingField(null=True, blank=True)
    tags = TaggableManager(blank=True)

    product_status= models.CharField(choices=STATUS, max_length=10, default='in_review')
    
    status =models.BooleanField(default=True)
    in_stock =models.BooleanField(default=True)
    featured =models.BooleanField(default=False)


    sku = ShortUUIDField(unique=True,length=4,max_length=10,prefix="sku",alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=True,blank=True)


    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price=(self.price/self.old_price)*100
        return new_price
    
class ProductImages(models.Model):
    images=models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product,related_name="p_images", on_delete=models.SET_NULL, null=True )
    date = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=50, default="Black")
   


    class Meta:
        verbose_name_plural = "Products Images"




################################### Cart,Order, OrderItems and Address #####################################        
################################### Cart,Order, OrderItems and Address #####################################        
################################### Cart,Order, OrderItems and Address #####################################        
################################### Cart,Order, OrderItems and Address #####################################        



class CartOrder(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)

    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    zip_code = models.CharField(max_length=20,null=True,blank=True)

    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address =models.CharField(max_length=255, blank=True, null=True)


    invoice_no = models.CharField(max_length=100, unique=True,  blank=True,null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=199)
    paid_status =models.BooleanField(default=False)
    order_date= models.DateTimeField(auto_now_add=True)
    product_status= models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')
    

    payment_method = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    def save(self, *args, **kwargs):
        if not self.invoice_no:
            while True:
                invoice = f"INV-{uuid.uuid4().hex[:8].upper()}"
                if not CartOrder.objects.filter(invoice_no=invoice).exists():
                    self.invoice_no = invoice
                    break
        super().save(*args, **kwargs)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name_plural = "Cart Order"

    def __str__(self):
        return self.invoice_no or "Order"


class CartOrderItems(models.Model):
        order= models.ForeignKey(CartOrder, on_delete=models.CASCADE,related_name="items")
        user= models.ForeignKey(User, on_delete=models.CASCADE)
       
        item= models.CharField( max_length=200)
        image= models.ImageField(upload_to="cart-order-items",default="")
       
        qty = models.IntegerField( default=1)
        price = models.DecimalField(max_digits=10, decimal_places=2, default=199)
        total = models.DecimalField(max_digits=10, decimal_places=2, default=199)
        size = models.CharField(max_length=50, blank=True, null=True)   # ✅ Add size
        color = models.CharField(max_length=50, blank=True, null=True)
        product_status = models.CharField(choices=STATUS_CHOICES,max_length=50, default="processing")


        class Meta:
            verbose_name_plural = "Cart Order Items"

        def order_img(self):
            return mark_safe(f'<img src="/media/%s" width="50" height="50" />'%(self.image))
        
        @property
        def invoice_no(self):
            return self.order.invoice_no


################################### Product Review Wishlist Address #####################################        


class ProductReview(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,related_name="reviews")
    review = models.TextField()
    rating =models.IntegerField(choices=RATING, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
        unique_together = ("user", "product")

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    




class Wishlist (models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100,null=True)
    mobile = models.CharField(max_length=100,null=True)
    status =models.BooleanField(default=False)
  



    

    class Meta:
        verbose_name_plural = "Address"







    

    


    

    
    

    

    





    
    
    
