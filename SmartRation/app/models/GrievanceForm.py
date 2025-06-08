from enum import Enum

class GrievanceForm:
    TABLE_NAME="grievanceform"
    def __init__(self):
        pass

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_last_update_date(self):
        return self.last_update_date

    def set_last_update_date(self, value):
        self.last_update_date = value

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_issue(self):
        return self.issue

    def set_issue(self, value):
        self.issue = value

    def get_staff_id(self):
        return self.staff_id

    def set_staff_id(self, value):
        self.staff_id = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def get_date_of_issue(self):
        return self.date_of_issue

    def set_date_of_issue(self, value):
        self.date_of_issue = value

    def get_family_id(self):
        return self.family_id

    def set_family_id(self, value):
        self.family_id = value

class GrievanceStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    REJECTED = "rejected"
    CLOSED = "closed"
    