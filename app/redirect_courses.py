from allImports import *
import sys

@app.route("/redirect/courses", methods=["GET", "POST"])
def redirectCourses():
   username = authUser(request.environ)
   user = User.get(User.username == username)
   if user.program != 0 and user.program is not None:
      subject = Subject.get(Subject.pid == user.program)
   else:
      subject = Subject.get()
   prefix = subject.prefix
   term = Term.get()
   termcode = term.termCode
   
   if request.method == "POST":
      data = request.form
      prefix   = data['prefix']
      termcode = int(data["term"])
      
   return redirect(url_for("courses", 
                           tID = termcode, 
                           prefix = prefix))
   
  
