from allImports import *

@app.route("/redirect/courses", met)
def redirectCourses():
   username = authUser(request.environ)
   user = User.get(User.username == username)
   
   if user.program != 0 and user.program is not None:
      program = user.program
   else:
      program = Program.get()
      
   print program.pID
   
   return "hello"
