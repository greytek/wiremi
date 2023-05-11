from fastapi import FastAPI, Request
import pyodbc
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
        cursor.execute("SELECT *from [wiremi].[dbo].[User]")
        rows = cursor.fetchall()
        print(rows)
        if rows[0] == 1:
            return {"message": "Database connected successfully"}
    except pyodbc.Error as ex:
        return {"message": f"Error connecting to the database: {str(ex)}"}
    finally:
        cursor.close()
        conn.close()

    return {"message": "Failed to connect to the database"}


@app.post("/users")
async def create_user(request: Request):
    try:
        query_params = dict(request)
        query_params = query_params['query_string']
        name, email, password, \
            user_type, \
            pin_code, phone_number = get_user_params(query_params)
        qr_code, wallet_id = get_qr_and_wallet(phone_number)

        driver.exec_store_proc(queries.sp_post_users,
                               [name, email, password, user_type, qr_code, pin_code, wallet_id, phone_number])
        return {"message": "User Registration successful"}
    except Exception as e:
        print(e)
        return {"Error": e}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
