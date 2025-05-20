from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from app.supabase_config import supabase
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.dao.RationDao import *
from app.dao.FamilyDao import getFamilyById
from app.dao.UserDetailDao import get_user_by_id,get_all_staff
from app.views.LoadView import get_staff_ration
from app.common.Util import get_current_date
from app.models import RationFamily
from app.common.email_util import send_custom_email,send_custom_html_email
# View for listing all ration records
def list_rations(request):
    try:
        ration_dict,isSuccess= get_all_rations()
        if isSuccess == False:
            messages.error(request, "Error fetching data!")
        for curr_list in ration_dict:
            staff_id=curr_list["staff"]
            print(staff_id)
            try:
                staffDetail=get_user_by_id(staff_id)
                curr_list["staff_name"]=staffDetail["user_name"]
            except Exception as e:
                curr_list["staff_name"] = "Not Assign"
                print("Ration error ",e)
        print(ration_dict)
        return render(request, "ration_list.html", {"rations": ration_dict})
    except Exception as e:
        messages.error(request, "Error fetching data!")
        return render(request, "ration_list.html", {"rations": []})
        

# View for creating a new ration entry
def add_ration(request):
    if request.method == "POST":
        address = request.POST.get("address")
        opening_days = request.POST.getlist('open_days')
        pincode = request.POST.get("pincode")
        try:
            data,error = create_ration(address, opening_days, pincode)
            messages.success(request, "Ration created successfully!")
            return redirect("list_ration")
        except Exception as e:
            print(e)
            messages.error(request, "Error creating ration!")
            return redirect("list_ration")
    return render(request, "ration_form.html")

# View for updating ration details
def edit_ration(request, ration_id):
    rationShop=None
    try:
        rationShop=get_ration_by_id(ration_id)
    except Exception as e:
        print("err ration shop",e)
    if request.method == "POST":
        staff = request.POST.get("staff")
        address = request.POST.get("address")
        opening_days = request.POST.getlist("open_days")
        print(opening_days)
        # opening_days=["monday","wednesday","friday"]
        pincode = request.POST.get("pincode")
        try:
            update_ration(ration_id, address, opening_days, pincode,staff)
            messages.success(request, "Ration updated successfully!")
            return redirect("list_ration")
        except Exception as e:
            messages.error(request, "Error updating ration!")
    all_days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    dayList=[0,0,0,0,0,0,0]
    i=1
    opening_days = rationShop['opening_days']
    for day in all_days:
        if day in opening_days:
            dayList[i-1]=i
        i=i+1
    print(dayList)
    print(rationShop)
    rationShop["dayList"]=dayList
    return render(request, "ration_form.html", {"rationShop": rationShop})

# View for deleting a ration record
def delete_ration_view(request, ration_id):
    try:
        messages.success(request, "Ration deleted successfully!")
        delete_ration(ration_id)
    except Exception as e:
        messages.error(request, "Error deleting ration!")
    return redirect("list_ration")

def assign_staff(request,ration_id):
    try:
        if request.method=="POST":
            staff_id=request.POST["staff"]
            if staff_id == "None":
                staff_id = None
            print("select staff ",staff_id)
            update_staff(ration_id,staff_id)
            messages.success(request, "Staff Assigned successfully!")
            return redirect("list_ration")
        rationShop=get_ration_by_id(ration_id)
        rationStaff={}
        rationStaff["rationShop"]=rationShop
        data,error=get_all_staff()
        rationStaff["staffList"]=data[1]
        return render(request, "assign_ration.html", rationStaff)
    except Exception as e:
        print(e)
        messages.warning(request, "Staff not Assign")
        return redirect("list_ration")
    
def list_ration_product(request):
    rationProducts=get_ration_product(request)
    return render(request,"ration_product.html",{"rationProducts":rationProducts})

def list_ration_families(request):
    ration=None
    try:
        ration=get_staff_ration(request)
    except Exception as e:
        print(e)
    rationFamilies=get_ration_families(request)
    return render(request,"ration_families.html",{"rationFamilies":rationFamilies,"ration":ration})

def distribute_product(request):
    rationProducts=get_ration_product(request)
    if request.method == 'POST':
        distribute_mail_send = request.POST.get('distribute_mail')
        distributeProductDictionary={}
        html_table_rows=""
        isSentMail = False
        body=""
        if distribute_mail_send == "sent":
            isSentMail = True
        for i in range(len(rationProducts)):
            product = rationProducts[i]
            distribute_quantity = float(request.POST.get("quantity_"+str(product["product_id"])))
            distributeProductDictionary[str(product["product_id"])]=distribute_quantity
            if isSentMail:
                html_table_rows += f"<tr><td>{product['product']['product_name']}</td><td>{product['product']['unit']}</td><td>{product['product']['price']}</td><td>{distribute_quantity}</td></tr>"
        if isSentMail:
            html_table ="<h1>இன்று பொருட்கள் விநியோகம் நடைபெறுகிறது - TNPDS </h1>"+form_html_table(html_table_rows)
            rationInfo=get_ration_detail(request)
            html_code =form_html_code(rationInfo+html_table)
            rationFamilies=get_ration_families(request)
            emails=[]
            for family in rationFamilies:
                emails.append(family['email'])
            print(html_code)
            send_custom_html_email(subject="இன்று ரேஷன் கடை திறந்திருக்கும்!",html=html_code,to_emails=emails)
        request.session["rationDistributeProduct"]=distributeProductDictionary
        return redirect("list_ration_families")
    distributeProduct=get_distribute_product(request)
    if rationProducts == None:
        messages.warning(request,"Please add ration product")
        return redirect("ration_products")
    setRationDistribute(request,rationProducts,distributeProduct)
    print(rationProducts)
    return render(request,"ration_distribution.html",{"rationProducts":rationProducts,"distributeproducts":distributeProduct})

def setRationDistribute(request,rationProducts,distributeProduct):
    if distributeProduct == None:
        distributeProduct={}
        for rationProduct in rationProducts:
            distributeProduct[str(rationProduct["product_id"])] = 0
            rationProduct["distribute_quantity"] = 0
        setDistributeProduct(request,distributeProduct)
    else:
        for rationProduct in rationProducts:
            try:
                distribute_quantity = distributeProduct[str(rationProduct["product_id"])]
                if  distribute_quantity != None:
                    rationProduct["distribute_quantity"] = distribute_quantity
                else:
                    rationProduct["distribute_quantity"] = 0
            except Exception as e:
                print(e)
                rationProduct["distribute_quantity"] = 0

def setDistributeProduct(request,distributeProduct):
    request.session["rationDistributeProduct"] = distributeProduct

def distribute_family_product(request,family_id):
    distributeProduct=get_distribute_product(request)
    rationProducts=get_ration_product(request)
    family=getFamilyById(family_id)
    if request.method == 'POST':
        distributedProductsDetail = ""
        rationDetail = get_ration_detail(request)
        html_table_rows=""
        for rationProduct in rationProducts:
            ration_stock_quantity = rationProduct["stock_quantity"]
            distribute_quantity = distributeProduct[str(rationProduct["product_id"])]
            new_quantity = float(ration_stock_quantity) - float(distribute_quantity)
            if distribute_quantity != 0 and (new_quantity > 0):
                rationProductObj = RationProduct()
                rationProductObj.set_ration_product_id(rationProduct["ration_product_id"])
                rationProductObj.set_product_id(rationProduct["product_id"])
                rationProductObj.set_ration_id(rationProduct["ration_id"])
                rationProductObj.set_last_update(get_current_date())
                rationProductObj.set_stock_quantity(new_quantity)
                updateRationProduct(rationProductObj)

                rationFamily=RationFamily.RationFamily()
                rationFamily.set_product_id(rationProductObj.get_product_id())
                rationFamily.set_actual_quantity(distribute_quantity)
                rationFamily.set_family_id(family_id)
                rationFamily.set_issued_date(get_current_date())
                rationFamily.set_issued_quantity(distribute_quantity)
                rationFamily.set_ration_id(rationProductObj.get_ration_id())
                addProductsToFamily(rationFamily)
                html_table_rows += f"<tr><td>{rationProduct['product']['product_name']}</td><td>{rationProduct['product']['unit']}</td><td>{rationProduct['product']['price']}</td><td>{distribute_quantity}</td><td>{distribute_quantity}</td></tr>"
        html_table = form_html_table(html_table_rows)
        body = rationDetail+"<h1>குடும்பம் பெற்ற பொருட்களின் விவரம் (Family received product details)</h1>"+html_table
        body = body+"""
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSfKduKNfD9RNJTgR7sL63K8LrV1ReHjDLtAQewqSda-qLHTsQ/viewform?usp=header" style="font-size:16px; font-family: Arial, sans-serif; padding:10px 20px; border:none; border-radius:5px; background-color:#007BFF; color:#fff; cursor:pointer;">
             புகார் (Issue)
        </a>
        """
        html_code = form_html_code(body)
        send_custom_html_email(subject="இன்று ரேஷன் கடை திறந்திருக்கும்!",html=html_code,to_emails=[family['email']])
        return redirect("list_ration_families")
    if family==None:
        messages.warning(request,"Family not found")
        return redirect("list_ration_families")
    if distributeProduct == None or len(distributeProduct) != len(rationProducts):
        messages.warning(request,"Please select or click update distribute products")
        return redirect("distribute_product")
    elif check_ration_stock(rationProducts,distributeProduct) == False:
        messages.warning(request,"stock quantity less than distribute quanity please update")
        return redirect("distribute_product")
    else:
        for i in range(len(rationProducts)):
            product = rationProducts[i]
            distribute_quantity = distributeProduct[str(product["product_id"])]
            product["distribute_quantity"] = distribute_quantity
        print(rationProducts)
        return render(request,"ration_family_distribute.html",{"rationProducts":rationProducts,"family":family})
    
def check_ration_stock(rationProducts,distributeProduct):
    count=0
    for rationProduct in rationProducts:
        ration_stock_quantity = rationProduct["stock_quantity"]
        distribute_quantity = distributeProduct[str(rationProduct["product_id"])]
        new_quantity = float(ration_stock_quantity) - float(distribute_quantity)
        if (new_quantity > 0) or (distribute_quantity == 0) :
            count = count + 1
    print("count    ",count)
    print(len(rationProducts))
    if count == len(rationProducts):
        return True
    return False

def get_distribute_product(request):
    return request.session.get("rationDistributeProduct")

def get_ration_product(request):
    try:
        ration=get_staff_ration(request)
        rationProducts=get_ration_products(ration["ration_id"])
        return rationProducts
    except Exception as e:
        print(e)
    return None

def get_ration_distribute_history(request):
    try:
        ration=get_staff_ration(request)
        rationFamilies = getRationFamilies(ration["ration_id"])
        isTest = False
        for rationFamily in rationFamilies:
            if isTest==False:
                print(rationFamily)
                isTest=True
        return render(request,"ration_distributed_history.html",{"rationFamilies":rationFamilies})
    except Exception as e:
        print(e)
        return redirect("list_ration_families")

def get_ration_families(request):
    try:
        ration=get_staff_ration(request)
        rationFamilies=get_families(ration["ration_id"])
        print(rationFamilies)
        return rationFamilies
    except Exception as e:
        print(e)
    return None


def get_ration_detail(request):
    try:
        ration=get_staff_ration(request)
        print(ration)
        rationInfo=f"""
            <h1>ரேஷன் விவரங்கள் (Ration Details)</h1>
                <table border="1" cellspacing="0" cellpadding="5">
                    <tr>
                        <td>முகவரி (Address)</td>
                        <td>{ration['address']}</td>
                    </tr>
                    <tr>
                        <td>அஞ்சல் குறியீடு (Pincode)</td>
                        <td>{ration['pincode']}</td>
                    </tr>
                </table>

                <br>
        """
        ration_staff = get_user_by_id(ration['staff'])
        staffInfo = f"""
                <h1>ஊழியர் விவரங்கள் (Staff Details)</h1>
                <table border="1" cellspacing="0" cellpadding="5">
                 <tr>
                    <td>ஊழியர் (Staff)</td>
                    <td>{ration_staff['user_name']}</td>
                </tr>
                <tr>
                    <td>தொலைபேசி (Phone)</td>
                    <td>{ration_staff['phone_number']}</td>
                </tr>
                <tr>
                    <td>மின்னஞ்சல் (Email)</td>
                    <td>{ration_staff['email']}</td>
                </tr>

                </table>
                <br>
            """
        return rationInfo+staffInfo
    except Exception as e:
        print(e)
        return "<h1>No Ration details</h1>"
    
def form_html_table(html_table_rows):
    table_html = """
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
       <th>பொருள் (Product)</th>
        <th>அலகு (Unit)</th>
        <th>விலை (Price)</th>
        <th>மூல அளவு (Actual Quantity)</th>
        <th>வழங்கப்பட்ட அளவு (Issued Quantity)</th>

        </thead>
    """
    table_html+=html_table_rows
    table_html += "</table>"
    return table_html

def form_html_code(html_body):
    return f"""
    <html>
    <body>
        {html_body}
    </body>
    </html>
    """
