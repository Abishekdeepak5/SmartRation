from app.models import Family
from django.shortcuts import render, redirect
from app.dao.FamilyDao import *
from app.dao.RationDao import get_all_rations
from app.common.Util import generateRandom
from django.contrib import messages
from app.dao.FamilyDao import getFamilyById,add_issue
from app.dao.RationDao import get_ration_by_id
from app.dao.UserDetailDao import get_user_by_id
from app.common.Util import get_current_date
from app.models import GrievanceForm
from app.views.UserDetailsView import get_user
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
        return render(request,"family_list.html", {"families":families[1]})
        # return render(request,"family_list.html")
    except Exception as e:
        try:
            messages.error(request, "Error List Families .Message:"+e.message)
        except Exception as exception:
            messages.error(request, "Error List Families!")
    print(families)
    return render(request,"family_list.html")

def grievance_form(request,family_id):
    if request.method == "POST":
        try:
            formData = GrievanceForm.GrievanceForm()
            formData.set_issue(request.POST.get("issue"))
            formData.set_staff_id(request.POST.get("staff_id"))
            formData.set_description(request.POST.get("description"))
            formData.set_date_of_issue(get_current_date())
            formData.set_family_id(request.POST.get("family_id"))
            formData.set_status(GrievanceForm.GrievanceStatus.PENDING.value)
            formData.set_last_update_date(get_current_date())
            add_issue(formData)
            messages.success(request, "Issue raised successfully!")
        except Exception as e:
            messages.error(request, "Error List Families .Message:"+e.message)
        return redirect("home")
    try:
        return render(request,"grievance_form.html",get_family_info_dict(family_id))
    except Exception as e:
        print(e)
        return redirect("home")
    
def get_issues_list(request):
    try:
        grievance_list = get_all_issue()
        return render(request,"issues.html",{"issues":grievance_list})
    except:
        return redirect("home")
    
def update_issue_status(request,issue_id):
    try:
        if request.method == "POST":
            description = request.POST.get("description")
            status = request.POST.get("status")
            logged_user = get_user(request)
            staff_id = logged_user["user_id"]
            edit_status(issue_id,{"last_update_date":get_current_date(),"staff_id":staff_id,"description":description,"status":GrievanceForm.GrievanceStatus(status).value})
            return redirect("family_issues")
        issueInfo = get_issue_by_id(issue_id)
        issueDict = get_family_info_dict(issueInfo["family_id"])
        issueDict["issueInfo"] = issueInfo
        issueDict["statusList"] = [(status.name, status.value) for status in GrievanceForm.GrievanceStatus]
        return render(request,"issue_update_form.html",issueDict)
    except Exception as e:
        print(e)
        return redirect("home")
    
def get_family_info_dict(family_id):
    family = getFamilyById(family_id)
    family_ration = get_ration_by_id(family["ration_id"])
    staff = get_user_by_id(family_ration["staff"])
    return {"family":family,"ration":family_ration,"staff":staff}


