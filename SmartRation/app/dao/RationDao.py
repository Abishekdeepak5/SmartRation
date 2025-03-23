from app.supabase_config import supabase

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
    return supabase.table("ration").select("*").execute()

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


