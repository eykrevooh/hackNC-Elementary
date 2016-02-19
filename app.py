import os

from app import app

if os.getenv('IP'):
  IP = os.getenv('IP')
else:
  IP = '0.0.0.0'

if os.getenv('PORT'):
  PORT = int(os.getenv('PORT'))
else:
  PORT = 8080

print ("Running at http://{0}:{1}/".format(IP, PORT))
app.run(host = IP, port = PORT, debug = True, threaded = True)

