class Product:
    # def __init__(self,product_id, product_name, unit, price, stock_quantity, tolerance, last_update):
    #     self.product_id=product_id
    #     self.product_name=product_name
    #     self.unit=unit
    #     self.price=price
    #     self.stock_quantity=stock_quantity
    #     self.tolerance=tolerance
    #     self.last_update=last_update

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, value):
        self.product_id = value

    def get_product_name(self):
        return self.product_name

    def set_product_name(self, value):
        self.product_name = value

    def get_unit(self):
        return self.unit

    def set_unit(self, value):
        self.unit = value

    def get_price(self):
        return self.price

    def set_price(self, value):
        self.price = value

    def get_stock_quantity(self):
        return self.stock_quantity

    def set_stock_quantity(self, value):
        self.stock_quantity = value

    def get_tolerance(self):
        return self.tolerance

    def set_tolerance(self, value):
        self.tolerance = value

    def get_last_update(self):
        return self.last_update

    def set_last_update(self, value):
        self.last_update = value
    def get_table_name(self):
        return "product"
    


