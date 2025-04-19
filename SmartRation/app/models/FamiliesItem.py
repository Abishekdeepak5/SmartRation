class FamiliesItem:
    def __init__(self,id, family_entitlement_id, item_id, actual_weight, status):
        self.id=id
        self.family_entitlement_id=family_entitlement_id
        self.item_id=item_id
        self.actual_weight=actual_weight
        self.status=status

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_family_entitlement_id(self):
        return self.family_entitlement_id

    def set_family_entitlement_id(self, value):
        self.family_entitlement_id = value

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, value):
        self.item_id = value

    def get_actual_weight(self):
        return self.actual_weight

    def set_actual_weight(self, value):
        self.actual_weight = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value
