class FamilyEntitlement:
    def __init__(self,id, family_id, date_of_issue):
        self.id=id
        self.family_id=family_id
        self.date_of_issue=date_of_issue

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_family_id(self):
        return self.family_id

    def set_family_id(self, value):
        self.family_id = value

    def get_date_of_issue(self):
        return self.date_of_issue

    def set_date_of_issue(self, value):
        self.date_of_issue = value

    
