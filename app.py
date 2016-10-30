'''
app.py is the starting point of the application; to run the app, in the console, you run "python app.py"

This file should not change often, except maybe to rename the application from "app" to something more meaningful
such as "helloWorldForm"

To rename the app, you need to make three changes:
1) Change  "from app import app" to "from helloWorldForm import app"
2) Rename the "app" folder to "helloWorldForm"
3) Rename this file to "helloWorldForm.py"

'''
import os,sys

from app import app


# print statements go to your log file in production; to your console while developing
app.run(host = '0.0.0.0', port = 5000)

