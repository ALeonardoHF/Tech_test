import os
from env_var import *

app_id = os.environ.get('APPLICATION_ID')
app_secret = os.environ.get('APPLICATION_SECRET')

print('1: ',app_id )
print('2: ', app_secret)