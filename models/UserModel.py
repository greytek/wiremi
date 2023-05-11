from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    pin_code: int
    qr_code: str
    wallet_id: str
    created_at: str
    user_type: str
    phone_number: str
