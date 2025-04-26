from app.supabase_config import supabase
from app.dao.DatabaseUtil import *
from app.models.Ration import Ration
from app.models.RationProduct import RationProduct
from app.models import Family
def create_ration(staff_id, address, opening_days, pincode):
    data, error = supabase.table("ration").insert({
        "staff": staff_id,
        "address": address,
        "opening_days": opening_days,  # Example: ['monday', 'tuesday']
        "pincode": pincode
    }).execute()
    
    if error:
        return {"success": False, "error": error}
    
    return {"success": True, "data": data}

def get_all_rations():
    try:
        data,error = supabase.table("ration").select("*").execute()
        return data[1],True
    except Exception as e:
        return [],False

def get_ration_by_id(ration_id):
        data, error = supabase.table("ration").select("*").eq("ration_id", ration_id).execute()
        return data[1][0]

def update_ration(ration_id, address=None, opening_days=None, pincode=None,staff=None):
    update_data = {}
    
    if address:
        update_data["address"] = address
    if opening_days:
        update_data["opening_days"] = opening_days
    if pincode:
        update_data["pincode"] = pincode
    if staff:
        update_data["staff"] = staff
    return supabase.table("ration").update(update_data).eq("ration_id", ration_id).execute()

def delete_ration(ration_id):
    supabase.table("ration").delete().eq("ration_id", ration_id).execute()

def update_staff(ration_id,staff_id):
    update_data={"staff":staff_id}
    return supabase.table("ration").update(update_data).eq("ration_id", ration_id).execute()

def get_ration_by_staff_id(staff_id):
    data,count=getRowsWithId(Ration.TABLE_NAME,'staff',staff_id)
    return data[1][0]  

def get_staff_ration(request):
    user=request.session.get("user")    
    ration=get_ration_by_staff_id(user["user_id"])
    return ration

def get_ration_products(ration_id):
    data,count = supabase.table(RationProduct.TABLE_NAME).select("*,product(*)").eq("ration_id", ration_id).execute()
    if len(data[1])==0:
        return None
    return data[1]

def get_families(ration_id):
    data,count = supabase.table(Family.Family.TABLE_NAME).select("*").eq("ration_id", ration_id).execute()
    if len(data[1])==0:
        return None
    return data[1]