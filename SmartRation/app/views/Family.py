from app.models import Family
from django.shortcuts import render, redirect
from app.dao.FamilyDao import *
from app.dao.RationDao import get_all_rations
from app.common.Util import generateRandom
from django.contrib import messages
import json
def add_family(request):
    if request.method == "POST":
        family = Family.Family()
        family.set_card_number(generateRandom())
        family.set_head_of_family(request.POST.get("head_of_family"))
        family.set_member_count(request.POST.get("member_count"))
        family.set_card_type(request.POST.get("card_type"))
        family.set_email(request.POST.get("email"))
        family.set_phone_number(request.POST.get("phone_number"))
        family.set_address(request.POST.get("address"))
        family.set_ration_id(request.POST.get("ration_id"))
        try:
            data,error = addFamily(family)
            messages.success(request, "Family Added successfully!")
            return redirect("list_ration")
        except Exception as e:
            if e.message:
                messages.error(request, "Error Adding Family.Message:"+e.message)
            else:
                messages.error(request, "Error Adding Family!")
            # return redirect("list_ration")
    ration,isSuccess = get_all_rations()
    if isSuccess:
        return render(request, "family_form.html",{"rations":ration})
    return render(request, "family_form.html")

def list_family(request,rationId):
    print(rationId)    
    try:
        families,error= get_ration_family(rationId)
        print(families[1])
        # {"families":families[1]}
        return render(request,"family_list.html", {"families":families[1]})
        # return render(request,"family_list.html")
    except Exception as e:
        try:
            messages.error(request, "Error List Families .Message:"+e.message)
        except Exception as exception:
            messages.error(request, "Error List Families!")
    print(families)
    return render(request,"family_list.html")