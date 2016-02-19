from allImports import *


@app.route("/", methods = ["GET"])
def main():
    print("Going to index")
    return render_template("index.html")
   