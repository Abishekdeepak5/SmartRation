from app.dao.DatabaseUtil import *

def addFamily(family):
    dict_data=family.__dict__
    # del dict_data['family_id']
    print(family)
    print(dict_data)
    return insertRow(family.get_table_name(),dict_data)

def get_ration_family(rationId):
    return getRowsWithId("families","ration_id",rationId)




















    # dict_data["family_id"]=family.get_family_id()
    # dict_data["card_number"]=family.get_card_number()
    # dict_data["head_of_family"]=family.get_head_of_family()
    # dict_data["member_count"]=family.get_member_count()
    # dict_data["card_type"]=family.get_card_type()
    # dict_data["email"]=family.get_email()
    # dict_data["phone_number"]=family.get_phone_number()
    # dict_data["address"]=family.get_address()
    # dict_data["ration_id"]=family.get_ration_id()
