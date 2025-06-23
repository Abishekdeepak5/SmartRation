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
from app.models import GrievanceForm,FamilyIssue,FamilyIssueLog
from app.views.UserDetailsView import get_user
from datetime import datetime
from django.utils import timezone

from app.views.summary import generate_overall_issues_summary, generate_dual_issue_summary
import pytz

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
            # formData = GrievanceForm.GrievanceForm()
            familyIssue = FamilyIssue.FamilyIssue()
            familyIssue.set_family_id(request.POST.get("family_id"))
            familyIssue.set_date_of_issue(get_current_date())
            familyIssue.set_issue(request.POST.get("issue"))
            familyIssue.set_status(GrievanceForm.GrievanceStatus.PENDING.value)
            addFamilyIssue(familyIssue)
            # formData.set_issue(request.POST.get("issue"))
            # formData.set_staff_id(request.POST.get("staff_id"))
            # formData.set_description(request.POST.get("description"))
            # formData.set_date_of_issue(get_current_date())
            # formData.set_family_id(request.POST.get("family_id"))
            # formData.set_status(GrievanceForm.GrievanceStatus.PENDING.value)
            # formData.set_last_update_date(get_current_date())
            # add_issue(formData)
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
    issues = get_all_family_issue()  # Your method to fetch all issues
    for issue in issues:
        issue["ai_summary"] = request.session.pop(f"summary_{issue['id']}", None)
        issue["error_msg"] = request.session.pop(f"error_{issue['id']}", None)
    total_summary = request.session.pop("total_summary", None)
    total_error = request.session.pop("total_error", None)
    selected_model = request.session.get("model_choice", "cohere")

    return render(request, "issues.html", {
        "issues": issues,
        "total_summary": total_summary,
        "total_error": total_error,
        "selected_model": selected_model,
    })


def generate_issue_summary_view(request):
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")
        model_choice = request.POST.get("model_choice", "cohere").strip()
        request.session["model_choice"] = model_choice

        try:
            if issue_id == "all":
                total_summary = generate_overall_issues_summary(model_choice=model_choice)
                request.session["total_summary"] = total_summary
            else:
                summary = generate_dual_issue_summary(issue_id=issue_id, model_choice=model_choice)
                request.session[f"summary_{issue_id}"] = summary
        except Exception as e:
            if issue_id == "all":
                request.session["total_error"] = str(e)
            else:
                request.session[f"error_{issue_id}"] = str(e)

    return redirect("issues")

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_issues_log_list(request, issue_id):
    issue_dict = {}
    try:
        issue_log = get_family_issue_log(issue_id)
        issue_info = get_family_issue_by_id(issue_id)
        issue_dict = get_family_info_dict(issue_info["family_id"])

        logs_sorted = sorted(issue_log, key=lambda x: x['last_update_date'])
        for log in logs_sorted:
            log['last_update_date'] = datetime.fromisoformat(log['last_update_date'])

        issue_dict["issueInfo"] = issue_info
        issue_dict["issue_id"] = issue_id
        issue_dict["logs"] = logs_sorted

        if request.method == "POST":
            model = request.POST.get("model_choice")
            try:
                summary = generate_dual_issue_summary(issue_id, model_choice=model)
                issue_dict["ai_summary"] = summary
                issue_dict["model_selected"] = model
                issue_dict["success_msg"] = "✅ AI Summary successfully generated using " + model.capitalize()
            except Exception as summary_err:
                issue_dict["error_msg"] = "❌ Failed to generate summary: " + str(summary_err)

        if request.GET.get("format") == "json":
            return JsonResponse(issue_dict, safe=False, json_dumps_params={'indent': 2, 'default': str})

        return render(request, "issue_logs.html", issue_dict)

    except Exception as e:
        return render(request, "issue_logs.html", {"error_msg": "❌ An unexpected error occurred: " + str(e)})    
def update_issue_status(request,issue_id):
    try:
        if request.method == "POST":
            description = request.POST.get("description")
            status = request.POST.get("status")
            logged_user = get_user(request)
            staff_id = logged_user["user_id"]
            kolkata_tz = pytz.timezone('Asia/Kolkata')
            now = timezone.now().astimezone(kolkata_tz)
            familyIssueLog = FamilyIssueLog.FamilyIssueLog()
            familyIssueLog.set_description(description)
            familyIssueLog.set_family_issue_id(issue_id)
            familyIssueLog.set_last_update_date(now.isoformat())
            familyIssueLog.set_staff_id(str(staff_id))
            familyIssueLog.set_status(GrievanceForm.GrievanceStatus(status).value)
            add_family_issue_log(familyIssueLog)

            # edit_status(issue_id,{"last_update_date":get_current_date(),"staff_id":staff_id,"description":description,"status":GrievanceForm.GrievanceStatus(status).value})
            edit_status(issue_id,{"status":GrievanceForm.GrievanceStatus(status).value})
            messages.success(request, "Issue updated successfully!")
            return redirect("family_issues")
        # issueInfo = get_issue_by_id(issue_id)
        issueInfo = get_family_issue_by_id(issue_id)
        issueDict = get_family_info_dict(issueInfo["family_id"])
        issueDict["issueInfo"] = issueInfo
        issueDict["statusList"] = [(status.name, status.value) for status in GrievanceForm.GrievanceStatus]
        return render(request,"issue_update_form.html",issueDict)
    except Exception as e:
        print(e)
        messages.error(request, "Error updating Issue .Message:"+e.message)
        return redirect("home")
    
def get_family_info_dict(family_id):
    family = getFamilyById(family_id)
    family_ration = get_ration_by_id(family["ration_id"])
    staff = get_user_by_id(family_ration["staff"])
    return {"family":family,"ration":family_ration,"staff":staff}


