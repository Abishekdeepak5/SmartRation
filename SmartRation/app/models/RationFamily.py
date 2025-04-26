

class RationFamily:
    def __init__(self,ration_family_id, ration_id, family_id, product_id, issued_quantity, issued_date):
        self.ration_family_id = ration_family_id
        self.ration_id = ration_id
        self.family_id = family_id
        self.product_id = product_id
        self.issued_quantity = issued_quantity
        self.issued_date = issued_date
        
    def get_ration_family_id(self):
        return self.ration_family_id

    def set_ration_family_id(self, value):
        self.ration_family_id = value

    def get_ration_id(self):
        return self.ration_id

    def set_ration_id(self, value):
        self.ration_id = value

    def get_family_id(self):
        return self.family_id

    def set_family_id(self, value):
        self.family_id = value

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, value):
        self.product_id = value

    def get_issued_quantity(self):
        return self.issued_quantity

    def set_issued_quantity(self, value):
        self.issued_quantity = value

    def get_issued_date(self):
        return self.issued_date

    def set_issued_date(self, value):
        self.issued_date = value

