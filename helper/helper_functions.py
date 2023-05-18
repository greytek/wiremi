from urllib.parse import parse_qs
import secrets
import string
import qrcode
import base64
from io import BytesIO


def get_user_params(params):
    name = params['name']
    email = params['email']
    password = params['password']
    user_type = params['user_type']
    pin_code = params['pin_code']
    phone_number = params['phone_number']
    if params['company_name']:
        company_name = params['company_name']
    else:
        company_name = ''
    if params['industry']:
        industry = params['industry']
    else:
        industry = ''
        print(name, email, password, user_type, pin_code, phone_number, company_name, industry)
    return name, email, password, user_type, pin_code, phone_number, company_name, industry


def get_qr_and_wallet(phone_number):
    user_data = phone_number
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(user_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    qr_code = base64.b64encode(buffered.getvalue())
    alphabet = string.ascii_letters + string.digits
    wallet_key = ''.join(secrets.choice(alphabet) for i in range(40))
    return qr_code, wallet_key
