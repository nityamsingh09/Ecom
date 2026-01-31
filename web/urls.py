from django.urls import path
from web import views
from .views import CreatePaymentView
app_name = 'web'
urlpatterns = [
    #Homepage
    path("",views.index,name="index"),
    path("products/",views.product_list_view,name="product-list"),
    path("products/<pid>",views.product_detail_view,name="product-detail"),
    
   # path("sign-up/",views.registration_view,name="sign-up"),

    #category
    path("category/",views.category_list_view,name="category-list"),
    path("category/<cid>/",views.category_product_list_view,name="category-product-list"),

    #vendor
    path("vendors/",views.vendor_list_view,name="vendor-list"),
    path("vendors/<vid>",views.vendor_detail_view,name="vendor-detail"),

    #tags
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),

    # ADD Review
    path("ajax-add-review/<int:pid>/" , views.ajax_add_review, name="ajax-add-review"),

    # Search
    path("search/", views.search_view, name="search"),

    #add_to_cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),

    path("cart/", views.cart_view, name="cart"),

    #delete item from cart
    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),

    #checkout
    path("checkout/", views.checkout_view, name="checkout"),

    # buy nou button
    path("buy-now/", views.buy_now, name="buy_now"),

    # payment view
        path(
        "create-payment/",
        CreatePaymentView.as_view(),
        name="create-payment"
    ),
    # payment success and failed
    path("payment-success/", views.payment_success, name="payment-success"),
    path("payment-failed/", views.payment_failed, name="payment-failed"),
    path(
    "payment-success-cod/",
    views.payment_success_cod,
    name="payment-success-cod"
),


    # download invoice
    path(
    "download-invoice/<str:order_id>/",
    views.download_invoice,
    name="download-invoice"
),

    path("dashboard/", views.customer_dashboard, name="dashboard"),
    path("dashboard/order/<int:id>/", views.order_detail_view, name="order-detail"),

####### make default address #########
    path("make-default-address/", views.make_address_default, name="make-default-address"),
    path("contact/", views.contact, name="contact-us"),
    path("ajax-contact-form/",views.ajax_contact_form, name="ajax-contact-form"),


    


]
