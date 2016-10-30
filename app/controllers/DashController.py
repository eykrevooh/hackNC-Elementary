# Dashboard Controller
from app.allImports import *


@app.route('/dashboard/', methods=["GET"])
def dash():
    working = Ta.select()\
            .join(User, on=(Ta.uID_id == User.uID))\
            .where(Ta.working == 1)
    return render_template('index.html',
                           working = working)
