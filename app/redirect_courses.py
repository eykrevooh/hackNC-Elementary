from allImports import *
import sys
import pprint

@app.route("/redirect/courses", methods=["GET", "POST"])
def redirectCourses():
   username = authUser(request.environ)
   user = User.get(User.username == username)
   if user.program != 0 and user.program is not None:
      subject = Subject.get(Subject.pid == user.program)
   else:
      subject = Subject.get()
   prefix = subject.prefix
   currentTerm = 0
   
   for t in Term.select():
      if t.termCode > currentTerm:
         currentTerm = t.termCode

   if request.method == "POST":
      data = request.form
      prefix   = data['prefix']
      currentTerm = int(data["term"])
      
   return redirect(url_for("courses", 
                           tID = currentTerm, 
                           prefix = prefix))
   
  
