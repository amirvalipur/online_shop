from random import randint
import os
from uuid import uuid4
from kavenegar import *

try:
    import json
except ImportError:
    import simplejson as json


def create_random_code(number):
    start = 10 ** (number - 1)
    end = (10 ** number) - 1
    active_code = randint(start, end)
    return active_code


def send_sms(receptor, active_code, message):
    APIKey = '----------------------------------------------------------'
    try:
        api = KavenegarAPI(APIKey)
        params = {
            'receptor': receptor,
            'message': message
        }
        response = api.sms_send(params)
        print(str(response))

    except APIException as e:
        print(str(e))
    except HTTPException as e:
        print(str(e))


# ____________________________________________________ delivery _ tax
def price_by_delivery_tax(price, discount=0):
    delivery = 30000
    if price > 1000000:
        delivery = 0
    tax = 0
    sum = price + delivery + tax
    sum = sum - (price * discount / 100)
    return int(sum), delivery, int(tax)


# __________________________________________________________

class FileUpload:
    def __init__(self, dir, prefix):
        self.dir = dir
        self.prefix = prefix

    def upload_to(self, instance, file_name):
        text, ext = os.path.splitext(file_name)
        random_name = uuid4()
        return f'{self.dir}/{self.prefix}/{random_name}{ext}'
