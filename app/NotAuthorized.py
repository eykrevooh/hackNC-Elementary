from allImports import *

@app.errorhandler(403)
def pageNotFound(e):
    return render_template('403.html', cfg=cfg), 403