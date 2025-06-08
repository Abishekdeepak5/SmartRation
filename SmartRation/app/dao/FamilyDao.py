from app.dao.DatabaseUtil import *
from app.models import Family,GrievanceForm
def addFamily(family):
    dict_data=family.__dict__
    # del dict_data['family_id']
    print(family)
    print(dict_data)
    return insertRow(Family.Family.TABLE_NAME,dict_data)

def get_ration_family(rationId):
    return getRowsWithId("families","ration_id",rationId)

def getFamilyById(family_id):
    data,count = getRowsWithId(Family.Family.TABLE_NAME,"family_id",family_id)
    try:
        return data[1][0]
    except Exception as e:
        print(e)
    return None

def getFamilyByCardNumber(card_number):
    data,count = getRowsWithId(Family.Family.TABLE_NAME,"card_number",card_number)
    try:
        return data[1][0]
    except Exception as e:
        print(e)
    return None

def add_issue(grievanceData):
    return insertRow(GrievanceForm.GrievanceForm.TABLE_NAME,grievanceData.__dict__)

def get_all_issue():
    data,count = getRows(GrievanceForm.GrievanceForm.TABLE_NAME)
    return data[1]

def get_issue_by_id(issue_id):
    data,count = getRowsWithId(GrievanceForm.GrievanceForm.TABLE_NAME,"id",issue_id)
    return data[1][0]

def edit_status(issue_id,issueUpdateDict):
    return updateRow(GrievanceForm.GrievanceForm.TABLE_NAME,issueUpdateDict,"id",issue_id)












    # dict_data["family_id"]=family.get_family_id()
    # dict_data["card_number"]=family.get_card_number()
    # dict_data["head_of_family"]=family.get_head_of_family()
    # dict_data["member_count"]=family.get_member_count()
    # dict_data["card_type"]=family.get_card_type()
    # dict_data["email"]=family.get_email()
    # dict_data["phone_number"]=family.get_phone_number()
    # dict_data["address"]=family.get_address()
    # dict_data["ration_id"]=family.get_ration_id()
