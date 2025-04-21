class RationProduct:
    TABLE_NAME="ration_product"
    # , ration_product_id, ration_id, product_id, stock_quantity, last_update
    def __init__(self):
        pass
        # self.ration_product_id = ration_product_id
        # self.ration_id = ration_id
        # self.product_id = product_id
        # self.stock_quantity = stock_quantity
        # self.last_update = last_update

    def get_ration_product_id(self):
        return self.ration_product_id

    def set_ration_product_id(self, value):
        self.ration_product_id = value

    def get_ration_id(self):
        return self.ration_id

    def set_ration_id(self, value):
        self.ration_id = value

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, value):
        self.product_id = value

    def get_stock_quantity(self):
        return self.stock_quantity

    def set_stock_quantity(self, value):
        self.stock_quantity = value

    def get_last_update(self):
        return self.last_update

    def set_last_update(self, value):
        self.last_update = value
