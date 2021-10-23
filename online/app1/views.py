from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Auther_Class, Product_class, Customer_Class,Feedback_form,Orders
from django.views.decorators.csrf import csrf_exempt
from Pay import Checksum
from django.urls import reverse






#email
import smtplib
import email.message

import qrcode
from django.conf import settings

#time
import time
from datetime import datetime, timezone
import pytz

MERCHANT_KEY = '@BLNEQSVwvSAf36N'
MERCHANT_ID = 'DSpKiN27217000419407'

# Create your views he

############################################ Customer  #########################################

def Index(request):
    if "User" in request.session.keys():
        print(request.session.keys())
        em = request.session['User']
        cust_user = Customer_Class.objects.get(cust_email=em)
        obj = Product_class.objects.all()
        return render(request,"index.html",{'data':obj,'customer':cust_user})
    else:
        obj = Product_class.objects.all()
        return render(request,'login.html')


def cart(request):
    return render(request,'cart.html')


def checkout(request):
    return render(request,'checkout.html')

def shop(request):
    return render(request,'shop.html')


def about(request):
    return render(request,'about.html')

def contactUs(request):
    if "User" in request.session.keys():
        em = request.session['User']
        cust_user = Customer_Class.objects.get(cust_email=em)
        if request.POST:
            obj = Feedback_form()
            obj.Name = request.POST['name']
            obj.email = request.POST['email']
            obj.sub = request.POST['subject']
            obj.mess = request.POST['message']  
            obj.save() 
            return redirect('index') 

           
        return render(request,'contact-us.html',{'customer':cust_user})
    else:
        print(request.session.keys())
        return redirect('index')


def login(request):
    if request.POST:
        em = request.POST['Email']
        ps = request.POST['Password']
        print(em,ps)
        try:
            data = Customer_Class.objects.get(cust_email=em)
            if data.cust_password == ps:
                request.session['User'] = data.cust_email
                return redirect('index')
            else:
                messages.warning(request, 'Password is Wrong ...')
                messages.warning(request, 'Try Something Else ...')
        except:
            messages.warning(request, 'Email Is Not Registered ...')
        
    return render(request,'login.html')

def reg(request):
    if request.POST:
        unm = request.POST['Username']
        em = request.POST['email']
        no = request.POST['no']
        ps1 = request.POST['password_1']
        ps2 = request.POST['password_2']
        
        try:
            val = Customer_Class.objects.get(cust_email=em)
            messages.warning(request, 'Email Id Already Exists ...')
        except: 
            if ps1 == ps2:
                obj = Customer_Class()
                obj.cust_name = unm
                obj.cust_email = em
                obj.cust_m_no = no
                obj.cust_password = ps1
                obj.save()               
                return redirect('login')
            else:
                messages.warning(request, 'Password Not Same ...')
    return render(request,'reg.html')

def forget(request):
    return render(request,'forget.html')

def orders(request):
    if request.session.keys():
        tot = 0
        user = Customer_Class.objects.get(cust_email=request.session['User'])
        show_data = Orders.objects.all().filter(name=user)
        for i in show_data:
            tot += i.pro_price 
        request.session['Order_total']=tot
  
        return render(request,'orders.html',{'data':show_data,'total':tot,'User':user.cust_name})
    else:
        return redirect('login')

def auther_View(request,id):
    if "User" in request.session.keys():
        em = request.session['User']
        cust_user = Customer_Class.objects.get(cust_email=em)
        auth = Auther_Class.objects.get(id=id)
        data = Product_class.objects.all().filter(auther=auth)
        return render(request,"author_view.html",{'data':data,'name':auth,'customer':cust_user}) 
    else:
        print(request.session.keys())
        return redirect('login')

def Customer_logout(request):
    if "User" in request.session.keys():
        del request.session['User']
        return redirect('aindex')
    else:
        print(request.session.keys())
        return redirect('login')


#################################################### Artist    ##################################3

def alogin(request):
    if request.POST:
        em = request.POST['Email']
        ps = request.POST['Password']
        print(em,ps)
        try:
            data = Auther_Class.objects.get(email=em)
            if data.password == ps:
                request.session['author']=data.email
                return redirect('aindex')
            else:
                messages.warning(request, 'Password is Wrong ...')
                messages.warning(request, 'Try Something Else ...')
        except:
            messages.warning(request, 'Email Is Not Registered ...')
    return render(request,'alogin.html')




def areg(request):
    if request.POST:
        unm = request.POST['Username']
        em = request.POST['email']
        ps1 = request.POST['password_1']
        ps2 = request.POST['password_2']
        
        try:
            val = Auther_Class.objects.get(email=em)
            # return HttpResponse("<h1><a href="">Already Exists ...</a></h1>")
            messages.warning(request, 'Email Id Already Exists ...')
        except:
            if ps1 == ps2:
                obj = Auther_Class()
                obj.name = unm
                obj.email = em
                obj.password = ps1
                obj.save()                
                return redirect('alogin')
            else:
                messages.warning(request, 'Password Not Same ...')
    return render(request,'areg.html')

    

def aforget(request):
    return render(request,'aforget.html')

def aproducts(request):
    if "author" in request.session.keys():
        em = request.session['author']
        auth = Auther_Class.objects.get(email=em)
        prod = Product_class.objects.filter(auther=auth)
        return render(request,'prod.html',{'prod':prod,'auth':auth})
    else:
        print(request.session.keys())
        return redirect('alogin')

def Add_Product(request):
    if "author" in request.session.keys():
        if request.POST:
            inm = request.POST['img_name']
            ipr = request.POST['img_price']
            idt = request.POST['img_details']
            img = request.FILES['img']
            
            obj = Product_class()
            em = request.session['author']
            obj.auther = Auther_Class.objects.get(email=em)
            obj.pro_name = inm
            obj.pro_price = ipr
            obj.pro_image = img
            obj.pro_detail = idt
            obj.save()
            return redirect('aindex')
            
        data = Auther_Class.objects.get(email=request.session['author'])
        return render(request,'add_product.html',{'data':data})
    else:
        return redirect('login')



def aindex(request):
    if "author" in request.session.keys():
        data = Auther_Class.objects.get(email=request.session['author'])
        prod = Product_class.objects.filter(auther=data)
        return render(request,'aindex.html',{'data':data,'prod':prod})
    else:
        
        return redirect('alogin')




def Auther_Products(request):
    if "author" in request.session.keys():
        em = request.session['author']
        auth = Auther_Class.objects.get(email=em)
        prod = Product_class.objects.filter(auther=auth)
        return render(request,'product.html',{'prod':prod,'auth':auth})
    else:
        print(request.session.keys())
        return redirect('login')



def Auther_Gallery(request):
    if "author" in request.session.keys():
        em = request.session['author']
        auth = Auther_Class.objects.get(email=em)
        prod = Product_class.objects.filter(auther=auth)
        return render(request,'gallery.html',{'pro_img':prod,'auth':auth})
    else:
        print(request.session.keys())
        return redirect('alogin')

def Update_Product(request,id):
    if "author" in request.session.keys():
        prod = Product_class.objects.get(id=id)
        auth = Auther_Class.objects.get(email=request.session['author'])
        if request.POST:
            inm = request.POST['img_name']
            ipr = request.POST['img_price']
            idt = request.POST['img_details']
            img = request.FILES.get('img')
            
            if img == None:
                img = prod.pro_image
                print(img)
    
            em = request.session['author']
            prod.author = Auther_Class.objects.get(email=em)
            prod.pro_name = inm
            prod.pro_price = ipr
            prod.pro_image = img
            prod.pro_detail = idt
            prod.save()
            return redirect('aindex')
        return render(request,'add_product.html',{'prod':prod,'auth':auth})
    else:
        return redirect('login')

def Auther_Logout(request):
    if "author" in request.session.keys():
        del request.session['author']
        return redirect('login')
    else:
        print(request.session.keys())
        return redirect('alogin')

def Delete_product(request ,id):
    prod=Product_class.objects.get(id=id)
    prod.delete()
    return redirect('aindex')



def Checkavailability(request):
    art = request.POST['name'].strip()
    artcount =Auther_Class.objects.filter(name__icontains = name).count()
    return render(request,'index.html',{ 'art':art,'foodcount':artcount})

def cart_remove(request,id):
    product = Orders.objects.get(id=id)
    product.delete()
    return redirect('order')


def place_order(request,id):
    
    cart = Orders()
    user = Customer_Class.objects.get(cust_email=request.session['User'])
    product = Product_class.objects.get(id=id)
    # product = get_object_or_404(Orders, id=id)
    try:
        print("nitin")
        # cd = Orders.cleaned_data
        cart.name = user
        cart.pro_name = product.pro_name
        cart.qty = 1
        cart.pro_price = product.pro_price
        cart.save()
        return redirect('orders')
    except:
        return redirect('index')


def Checkout(request,mode):
    #time Zone
    tz= pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    order_id = "Orders"+str(millis)
    request.session['Order_id'] = order_id
    
    if mode == 'pytm':
        return redirect('process_payment')
    else:
        return redirect('paycash')


def EmailCall(request):

    user = Customer_Class.objects.get(cust_email=request.session['User'])
    show_data = Orders.objects.all().filter(name=user)
    amo = request.session['Order_total']
    print(amo)
    order_id = request.session['Order_id']
    
    my_email = "namarataverma123456@gmail.com"
    my_pass = "namaratanimi"
    fr_email = str(user.cust_email)
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    mead_data = ""
    front = """
    <!DOCTYPE html>
    <html>
        <body>
            <div>
                <h2>Name : """ + user.cust_name + """</h2>
                <h2>Email : """ + user.cust_email + """</h2>
                <h2>Order No: """ + order_id + """</h2>
            </div>
            <br>
            <div>
                <table border="2">
                    <thead>
                        <tr>
                            <th>
                                Product Name
                            </th>
                            <th>
                                Product Qty
                            </th>
                            <th>
                                Product Price
                            </th>
                        </tr>
                    </thead>
                    <tbody>"""
                    
    for i in show_data:
        mead_data += """<tr>
        <td>""" + str(i.pro_name) + """ </td>
        <td>""" + str(i.qty) + """ </td> 
        <td>""" + str(i.pro_price) + """</td></td>
        </tr> """
        
    ended = """<tr>
    <td colspan="2">
    You Have Paid
    </td><td> """ + str(amo) + """
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div> 
            <br>
            <div>
                <h3>Thank you for visiting ....</h3>
            </div>
        </body>
    </html>
    """
    email_content = front + mead_data + ended
    print(email_content)
    
    msg = email.message.Message()
    msg['Subject'] = 'Your Bill' 
    msg['From'] = my_email
    msg['To'] = fr_email
    password = my_pass
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    

    

    show_data.delete()
        
    return redirect('index')

def qrcode(request,id):
    if "User" in request.session.keys():
        user = Customer_Class.objects.get(cust_email=request.session['User'])
        show_data = Orders.objects.all().filter(name=user)
        amo = request.session['Order_total']
        print(amo)
        order_id = request.session['Order_id']
        
    
        mead_data = ""
        front = """
        <!DOCTYPE html>
        <html>
            <body>
                <div>
                    <h2>Name : """ + user.cust_name + """</h2>
                    <h2>Email : """ + user.cust_email + """</h2>
                    <h2>Order No: """ + order_id + """</h2>
                </div>
                <br>
                <div>
                    <table border="2">
                        <thead>
                            <tr>
                                <th>
                                    Product Name
                                </th>
                                <th>
                                    Product Qty
                                </th>
                                <th>
                                    Product Price
                                </th>
                            </tr>
                        </thead>
                        <tbody>"""
                        
        for i in show_data:
            mead_data += """<tr>
            <td>""" + str(i.pro_name) + """ </td>
            <td>""" + str(i.qty) + """ </td> 
            <td>""" + str(i.pro_price) + """</td></td>
            </tr> """
            
        ended = """<tr>
        <td colspan="2">
        You Have Paid
        </td><td> """ + str(amo) + """
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div> 
                <br>
                <div>
                    <h3>Thank you for visiting ....</h3>
                </div>
            </body>
        </html>
        """  
        data=front+mead_data+ended 
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
            
        qrcode_nm ="new_QRcode.jpg"
        qrcode_path = settings.MEDIA_ROOT+"/"+qrcode_nm
        print(qrcode_path)
        img.save(qrcode_path)
            
        val = "/media/qrcode/"+qrcode_nm
            
        return render(request,'View_QRCode.html',{'Da':val})
            
    else:
        return redirect('login')
@csrf_exempt
def Handlerequest(request):
    # paytm will send you post request here
    
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful') 
            return redirect('emailcall')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            
    return render(request, 'paymentsatus.html', {'response': response_dict})

def PayCash(request):
    return render(request,'success.html')            

def Process_payment(request):
    user =Customer_Class .objects.get(cust_email=request.session['User'])
    show_data = Orders.objects.all().filter(name=user)
    amo = request.session['Order_total']
    host = request.get_host()
    param_dict = {
        'MID': MERCHANT_ID,
        'ORDER_ID': str(request.session['Order_id']),
        'TXN_AMOUNT': str(amo),
        'CUST_ID': 'darpan_salunke',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://{}{}'.format(host,reverse('handlerequest')),
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict,'User':user,'Order':show_data})


