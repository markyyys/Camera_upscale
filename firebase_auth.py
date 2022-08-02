import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBdJuSUO7osFFJoEXAQZEGfGjjulJl-E30",
    "authDomain": "neural-network-7a356.firebaseapp.com",
    "databaseURL": "https://neural-network-7a356.firebaseio.com",
    "projectId": "neural-network-7a356",
    "storageBucket": "neural-network-7a356.appspot.com",
    "messagingSenderId": "622588999161",
    "appId": "1:622588999161:web:2f1e4a1ee2fc7cc2a07928"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def login(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
    except:
        return False
    return True

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
    except:
        return False
    return True
