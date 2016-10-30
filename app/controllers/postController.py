#Post question controller

from app.allImports import *

@app.route('/post/', methods=["GET","POST"])
def postQuestion():
    if request.method == 'POST':
        #TODO: set values posted by form for question table
        pass
    return render_template('postView.html')
