from django.contrib import admin
from .models import Customer_Class,Auther_Class,Product_class,Feedback_form,Orders


admin.site.register(Auther_Class)
admin.site.register(Customer_Class)
admin.site.register(Product_class)
admin.site.register(Feedback_form)
admin.site.register(Orders)

