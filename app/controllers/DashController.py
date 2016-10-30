# Dashboard Controller
from app.allImports import *


@app.route('/dashboard/<perm>', methods=["GET"])
def dash(perm):
    print perm
    working = Ta.select()\
            .join(User, on=(Ta.uID_id == User.uID))\
            .where(Ta.working == 1)
    return render_template('dash.html',
                           working = working,user=perm)
