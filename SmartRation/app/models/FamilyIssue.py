class FamilyIssue:
    TABLE_NAME="familyissue"
    def __init__(self):
        pass

    def id(self):
        return self.id

    def id(self, value):
        self.id = value

    def family_id(self):
        return self.family_id

    def set_family_id(self, value):
        self.family_id = value

    def issue(self):
        return self.issue


    def set_issue(self, value):
        self.issue = value

    def date_of_issue(self):
        return self.date_of_issue

    def set_date_of_issue(self, value):
        self.date_of_issue = value

    def set_status(self,value):
        self.status = value
        
    def get_status(self):
        return self.status
 