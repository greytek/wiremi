import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pyodbc
from db.conn import connection_string
from Executor import driver, queries
from helper.helper_functions import get_user_params, get_qr_and_wallet

app = FastAPI()

conn = pyodbc.connect(connection_string)


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
        cursor.close()
        conn.close()

    return {"message": "Failed to connect to the database"}


@app.post("/register_users")
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
                                        [name, email, password, user_type, qr_code, pin_code, wallet_id, phone_number, company_name, industry])
            return {"message": "Business Registration successful"}
    except Exception as e:
        print(e)
        return {"Error": e}


@app.get("/get_users")
async def get_users():
    try:
        user_data = driver.exec_query(queries.get_users_from_db, is_col_required=True)
        user_data = user_data.to_json(orient='records')
        return JSONResponse(json.loads(user_data), status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)


@app.delete("/delete_users")
async def delete_user():
    try:
        user_data = driver.exec_query(queries.get_users_from_db, is_col_required=True)
        user_data = user_data.to_json(orient='records')
        return JSONResponse(json.loads(user_data), status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)


@app.get("/login_users")
async def login_user(request: Request):
    try:
        attr = await request.form()
        pn = attr['phone_number']
        pw = attr['password']
        verify = driver.exec_store_proc_get(queries.sp_verify_user, [pn, pw], is_col_required=False)
        return JSONResponse(verify[0][0], status_code=200)
    except Exception as e:
        return JSONResponse(e, status_code=404)
