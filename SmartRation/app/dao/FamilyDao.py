from app.dao.DatabaseUtil import *
from app.models import Family,GrievanceForm,FamilyIssue, FamilyIssueLog
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
    print(grievanceData.__dict__)
    return insertRow(GrievanceForm.GrievanceForm.TABLE_NAME,grievanceData.__dict__)

def addFamilyIssue(familyIssue):
    return insertRow(FamilyIssue.FamilyIssue.TABLE_NAME,familyIssue.__dict__)

def get_all_issue():
    data,count = getRows(GrievanceForm.GrievanceForm.TABLE_NAME)
    return data[1]

def get_all_family_issue():
    data,count = getRows(FamilyIssue.FamilyIssue.TABLE_NAME)
    return data[1]

def get_family_issue_log(issue_id):
    data,count = getRowsWithId(FamilyIssueLog.FamilyIssueLog.TABLE_NAME,"family_issue_id",issue_id)
    try:
        return data[1]
    except Exception as e:
        print(e)
    return None

def get_issue_by_id(issue_id):
    data,count = getRowsWithId(GrievanceForm.GrievanceForm.TABLE_NAME,"id",issue_id)
    return data[1][0]

def get_family_issue_by_id(issue_id):
    data,count = getRowsWithId(FamilyIssue.FamilyIssue.TABLE_NAME,"id",issue_id)
    return data[1][0]

# def edit_status(issue_id,issueUpdateDict):
#     return updateRow(GrievanceForm.GrievanceForm.TABLE_NAME,issueUpdateDict,"id",issue_id)

def edit_status(issue_id,issueUpdateDict):
    return updateRow(FamilyIssue.FamilyIssue.TABLE_NAME,issueUpdateDict,"id",issue_id)

def add_family_issue_log(familyIssueLog):
    print(familyIssueLog.__dict__)
    return insertRow(FamilyIssueLog.FamilyIssueLog.TABLE_NAME, familyIssueLog.__dict__)
