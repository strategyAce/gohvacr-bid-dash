import os
def authenticate(username, password):
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    return username == USERNAME and password == PASSWORD
