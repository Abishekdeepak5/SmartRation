class RationTransport:
    def __init__(self, ration_transport_id, load_send_date, load_received_date, status, ration_id):
        self.ration_transport_id = ration_transport_id
        self.load_send_date = load_send_date
        self.load_received_date = load_received_date
        self.status = status
        self.ration_id = ration_id

    def get_ration_transport_id(self):
        return self.ration_transport_id

    def set_ration_transport_id(self, value):
        self.ration_transport_id = value

    def get_load_send_date(self):
        return self.load_send_date

    def set_load_send_date(self, value):
        self.load_send_date = value

    def get_load_received_date(self):
        return self.load_received_date

    def set_load_received_date(self, value):
        self.load_received_date = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_ration_id(self):
        return self.ration_id

    def set_ration_id(self, value):
        self.ration_id = value

