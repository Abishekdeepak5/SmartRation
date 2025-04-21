from enum import Enum

class RationTransport:
    TABLE_NAME="ration_transport"
    def __init__(self):
        # self.ration_transport_id = None
        self.load_send_date = None
        self.load_received_date = None
        self.status = None
        self.ration_id = None

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
    def get_table_name(self):
        return "ration_transport"

class Status(Enum):
    LOADING = "loading"
    SEND = "send"
    RECEIVED = "received"
