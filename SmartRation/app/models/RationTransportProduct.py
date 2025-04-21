class RationTransportProduct:
    TABLE_NAME="ration_transport_product"
    def __init__(self):
        self.ration_transport_id = None
        self.product_id =None
        self.allocated_qty =None
        self.received_qty = None
        self.update_date=None

    def get_ration_transport_product_id(self):
        return self.ration_transport_product_id

    def set_ration_transport_product_id(self, value):
        self.ration_transport_product_id = value

    def get_ration_transport_id(self):
        return self.ration_transport_id

    def set_ration_transport_id(self, value):
        self.ration_transport_id = value

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, value):
        self.product_id = value

    def get_allocated_qty(self):
        return self.allocated_qty

    def set_allocated_qty(self, value):
        self.allocated_qty = value

    def get_received_qty(self):
        return self.received_qty

    def set_received_qty(self, value):
        self.received_qty = value
    
    def set_update_date(self, value):
        self.update_date = value

    def get_update_date(self):
        return self.update_date
