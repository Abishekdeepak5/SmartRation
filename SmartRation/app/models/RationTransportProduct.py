class RationTransportProduct:
    def __int__(self, ration_transport_product_id, ration_transport_id, product_id, allocated_qty, received_qty):
        self.ration_transport_product_id = ration_transport_product_id
        self.ration_transport_id = ration_transport_id
        self.product_id = product_id
        self.allocated_qty = allocated_qty
        self.received_qty = received_qty

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
