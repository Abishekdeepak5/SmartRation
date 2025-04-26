class Family:
    TABLE_NAME = "families"
    tableName="families"
    def __init__(self):
        pass

    def get_family_id(self):
        return self.family_id

    def set_family_id(self, value):
        self.family_id = value

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, value):
        self.card_number = value

    def get_head_of_family(self):
        return self.head_of_family

    def set_head_of_family(self, value):
        self.head_of_family = value

    def get_member_count(self):
        return self.member_count

    def set_member_count(self, value):
        self.member_count = value

    def get_card_type(self):
        return self.card_type

    def set_card_type(self, value):
        self.card_type = value

    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, value):
        self.phone_number = value

    def get_address(self):
        return self.address

    def set_address(self, value):
        self.address = value

    def get_ration_id(self):
        return self.ration_id

    def set_ration_id(self, value):
        self.ration_id = value

    def get_table_name(self):
        return self.tableName


    # def __init__(self,family_id, card_number, head_of_family, member_count, card_type, email, phone_number, address, ration_id):
    #     self.family_id=family_id
    #     self.card_number=card_number
    #     self.head_of_family=head_of_family
    #     self.member_count=member_count
    #     self.card_type=card_type
    #     self.email=email
    #     self.phone_number=phone_number
    #     self.address=address
    #     self.ration_id=ration_id