class StockRequest:
    def __init__(self):
        self.stock_id = stock_id
        self.ration_id = ration_id
        self.item_id = item_id
        self.quantity = quantity
        self.status = status

    def get_stock_id(self):
        return self.stock_id

    def set_stock_id(self, value):
        self.stock_id = value

    def get_ration_id(self):
        return self.ration_id

    def set_ration_id(self, value):
        self.ration_id = value

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, value):
        self.item_id = value

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, value):
        self.quantity = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value
