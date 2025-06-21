class FamilyIssueLog:
    TABLE_NAME="familyissuelog"
    def __init__(self):
        pass

    def id(self):
        return self.id

    def id(self, value):
        self.id = value

    def get_family_issue_id(self):
        return self.family_issue_id

    def set_family_issue_id(self, value):
        self.family_issue_id = value

    def get_last_update_date(self):
        return self.last_update_date

    def set_last_update_date(self, value):
        self.last_update_date = value

    def get_staff_id(self):
        return self.staff_id

    def set_staff_id(self, value):
        self.staff_id = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

