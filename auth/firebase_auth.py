import pyrebase

firebase_config = {
    "apiKey": "AIzaSyBNkr6npp8M4kgB6mMH709fBE9H8nnHaGk",
    "authDomain": "wiremi-db.firebaseapp.com",
    "databaseURL": "https://wiremi-db.firebaseio.com",
    "projectId": "wiremi-db",
    "storageBucket": "wiremi-db.appspot.com",
    "messagingSenderId": "494081107830",
    "appId": "wiremi-db"
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


async def register_user(email, password):
    user = auth.create_user_with_email_and_password(email, password)
    return user


async def authenticate_user(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print(login)
        # return {auth.get_account_info(login['idToken']), 'Logged In Successfully'}
        return {"message": "Login SuccesAsful"}
    except:
        return {"message": "Invalid email or password"}


async def reset_pass(email):
    try:
        auth.send_password_reset_email(email)
        return {"message": "Password reset email has been sent."}

    except Exception as e:
        return {"Exception": e}
