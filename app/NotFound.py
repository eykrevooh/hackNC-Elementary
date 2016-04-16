from allImports import *

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html', cfg=cfg), 404