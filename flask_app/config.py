
import os
my_secret = os.environ['atlas_username']
my_pass = os.environ['atlas_password']
# Stores all configuration values
SECRET_KEY = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'
MONGODB_HOST = "mongodb+srv://" + my_secret + ":" + my_pass + "@final.kk2kkml.mongodb.net/?retryWrites=true&w=majority"
