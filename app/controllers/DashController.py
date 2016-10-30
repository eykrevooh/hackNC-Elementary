# Dashboard Controller
from app.allImports import *


@app.route('/dashboard/<perm>', methods=["GET"])
@app.route('/dashboard/<perm>/<lab>', methods=["GET"])
def dash(perm, lab=None):
    if lab == "in":
        if Ta.select().where(Ta.working == 0).count() > 0:
            kye = Ta.get(Ta.working == 0)
            kye.working = 1
            kye.save()
    working = Ta.select()\
            .join(User, on=(Ta.uID_id == User.uID))\
            .where(Ta.working == 1)
    return render_template('dash.html',
                           working = working,user=perm)
