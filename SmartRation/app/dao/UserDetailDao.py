from app.supabase_config import supabase
from app.models import UserDetails
def get_user_by_email(email):
        return supabase.table("user_details").select("*").eq("email", email).execute() 

def register_user(user):
    return supabase.table("user_details").insert({
                "user_name":user.get_user_name() ,
                "password": user.get_password(),
                "role": user.get_role(),
                "phone_number": user.get_phone_number(),
                "gender": user.get_gender(),
                "email": user.get_email(),
                "address": user.get_address(),
                "pincode": user.get_pincode(),
                "date_of_birth": user.get_date_of_birth()
            }).execute()

def get_user_by_id(user_id):
        data,error=supabase.table("user_details").select("*").eq("user_id", user_id).execute()
        return data[1][0]
def get_all_staff():
        return supabase.table("user_details").select("*,ration(*)").eq("role","staff").execute()
