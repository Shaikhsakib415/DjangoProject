from django.urls import path
from .views import Index, about, cart, checkout, contactUs, shop,login,reg,forget,alogin,areg,aforget
from .views import aindex,aproducts,Add_Product,Auther_Gallery,orders,Update_Product,auther_View,Auther_Products
from .views import Auther_Logout,Customer_logout,Delete_product,Checkavailability,EmailCall,place_order,PayCash
from .views import Handlerequest,cart_remove,Checkout,Process_payment,qrcode
urlpatterns = [
    path('index',Index,name="index"),
    path('cart',cart,name="cart"),
    path('checkout',checkout,name="checkout"),
    path('shop',shop,name="shop"),
    path('about',about,name="about"),
    path('',login,name="login"),
    path('reg',reg,name="reg"),
    path('forget',forget,name="forget"),
    path('contactUs',contactUs,name="contactUs"),
    path('auther_view/<int:id>/',auther_View,name='auther_view'),
    path('Orders/',orders,name='orders'),
    path('logout/',Customer_logout,name='cust_logout'),
      
    path('alogin',alogin,name="alogin"),
    path('areg',areg,name="areg"),
    path('aforget',aforget,name="aforget"),
    path('update_product/<int:id>/',Update_Product,name="update_pro"),
    path('delete_product/<int:id>/',Delete_product,name="delete_product"),
    path('aindex',aindex,name="aindex"),
    path('add_prod/',Add_Product,name='add_prod'),
    path('auth_gallery/',Auther_Gallery,name='auth_gallery'),
    path('a_prod/',Auther_Products,name='a_prod'),
    path('auth_logout/',Auther_Logout,name='auth_logout'),

    path("checkavailability/",Checkavailability, name="checkavailability"),

    path('EmailCall/',EmailCall,name='emailcall'),
    path('PayCash/',PayCash,name='paycash'),
    path('Place_order/<int:id>',place_order,name='place_order'),
    path('payment_process/',Process_payment,name='process_payment'),
    path("handlerequest/",Handlerequest, name="handlerequest"),
    path('remove/<int:id>/',cart_remove, name='cart_remove'),
    path('check/<str:mode>',Checkout,name='check'),


    path("qrcode/<str:id>",qrcode,name="qrcode"),
    
    
]



