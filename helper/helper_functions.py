from urllib.parse import parse_qs
import secrets
import string
import qrcode
import base64
from io import BytesIO



def get_user_params(params):
    regular_str = params.decode('utf-8')
    attr = parse_qs(regular_str)
    name = ', '.join(attr['name'])
    email = ', '.join(attr['email'])
    password = ', '.join(attr['password'])
    user_type = ', '.join(attr['user_type'])
    pin_code = ', '.join(attr['pin_code'])
    phone_number = ', '.join(attr['phone_number'])
    return name, email, password, user_type, pin_code, phone_number


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
