import json
import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pyodbc
import stripe
from drivers.db.models import PaymentRequest
from drivers.db.conn import connection_string_live, connection_string_local
from executor import driver, queries
from drivers.helper.helper_functions import get_user_params, get_qr_and_wallet

app = FastAPI()

conn = pyodbc.connect(connection_string_live)


@app.get("/test")
async def test_db_connection():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT *from [dbo].[User]")
        rows = cursor.fetchall()
        if rows:
            return {"message": "Database connected successfully"}
    except pyodbc.Error as ex:
        return {"message": f"Error connecting to the database: {str(ex)}"}
    finally:
        conn.close()

    return {"message": "Failed to connect to the database"}


@app.post("/register_users", tags=["User"])
async def create_user(request: Request):
    try:
        attr = await request.form()
        name, email, password, user_type, pin_code, phone_number, company_name, industry = get_user_params(attr)
        qr_code, wallet_id = get_qr_and_wallet(phone_number)

        print(name, email, password, user_type, qr_code, pin_code, wallet_id, phone_number, company_name, industry)
        if user_type == 'student':
            driver.exec_store_proc_post(queries.sp_post_users_student,
                                        [name, email, password, user_type, qr_code, pin_code, wallet_id, phone_number])
            return {"message": "Student Registration successful"}
        if user_type == 'business':
            driver.exec_store_proc_post(queries.sp_post_users_business,
                                        [name, email, password, user_type, qr_code, pin_code, wallet_id, phone_number,
                                         company_name, industry])
            return {"message": "Business Registration successful"}
    except Exception as e:
        print(e)
        return {"Error": e}


@app.get("/get_users", tags=["User"])
async def get_users():
    try:
        user_data = driver.exec_query(queries.get_users_from_db, is_col_required=True)
        user_data = user_data.to_json(orient='records')
        return JSONResponse(json.loads(user_data), status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)


@app.delete("/delete_users", tags=["User"])
async def delete_user():
    try:
        user_data = driver.exec_query(queries.get_users_from_db, is_col_required=True)
        user_data = user_data.to_json(orient='records')
        return JSONResponse(json.loads(user_data), status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)


@app.get("/login_users", tags=["User"])
async def login_user(request: Request):
    try:
        attr = await request.form()
        pn = attr['phone_number']
        pw = attr['password']
        verify = driver.exec_store_proc_get(queries.sp_verify_user, [pn, pw], is_col_required=False)
        return JSONResponse(verify[0][0], status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)


@app.post("/payment")
async def process_payment(payment_request: PaymentRequest):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=payment_request.amount,
            currency="usd",
            source=payment_request.token,
            description="Payment for services"
        )

        # Process the payment and return a response
        response_data = {
            "status": "Payment successful",
            "charge_id": charge.id
        }
        return JSONResponse(content=jsonable_encoder(response_data))

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        error_message = e.user_message or str(e)
        raise HTTPException(status_code=400, detail=error_message)

    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    if conn:
        return {"Hello World from Wiremi Root and DB Connected"}
    return {"DB Not Connected"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.environ.get("PORT", 8111)), host="0.0.0.0", reload=True)
