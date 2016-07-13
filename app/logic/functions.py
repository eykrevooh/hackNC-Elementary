from app.allImports import *
conflicts = load_config(os.path.join(here, 'conflicts.yaml'))
'''
checks whether two schedules conflicts
@param {string} sid1 the schedule id of the first course
@param {string} sid2 the schedule id of the second schedule

@returns {boolean}
'''

def doesConflict(sid1, sid2):
    return conflicts[sid1][sid2]