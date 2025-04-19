import random
from datetime import datetime
def generateRandom():
    random_number = random.randint(10**11, 10**12 - 1)
    print("12-digit Random Number:", random_number)
    return random_number

def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')