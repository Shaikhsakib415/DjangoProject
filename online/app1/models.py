from django.db import models

# Create your models here.

class Customer_Class(models.Model):
    cust_name = models.CharField("User Name",default="",max_length=100)
    cust_m_no = models.PositiveIntegerField(verbose_name="Mobile no",default=00000000,max_length=10)
    cust_email = models.CharField(default="",max_length=100)
    cust_password = models.CharField(default="",max_length=100)
    
    def __str__(self):
        return self.cust_name
    
class Auther_Class(models.Model):
    img = models.ImageField(upload_to="profile/",blank=True,null=True)
    name = models.CharField("User Name",default="",max_length=100)
    m_no = models.PositiveIntegerField(verbose_name="Mobile no",default=00000000)
    email = models.CharField(default="",max_length=100)
    password = models.CharField(default="",max_length=100)
    
    def __str__(self):
        return self.name

class Product_class(models.Model):
    auther = models.ForeignKey('Auther_Class',default=0,on_delete=models.CASCADE)
    pro_name = models.CharField("Image Name",default="",max_length=100)
    pro_price = models.PositiveIntegerField("Image Price",default=0)
    pro_image = models.ImageField(upload_to="images/",blank=True)
    pro_detail = models.CharField(default="", max_length=200)
    
    def __str__(self):
        return self.pro_name



class Feedback_form(models.Model):
    Name = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=100,default="")
    sub = models.TextField(default="",max_length=100)
    mess = models.TextField(default="",max_length=500)
    def __str__(self):
        return self.Name

class Orders(models.Model):
    name = models.ForeignKey('Customer_Class',default=0,on_delete=models.CASCADE)
    pro_name = models.CharField(max_length=100,default="")
    qty = models.PositiveIntegerField(default=1)
    pro_price = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.name