{"changed":true,"filter":false,"title":"create_db.py","tooltip":"/create_db.py","value":"# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!\n'''\nThis script creates the database tables in the SQLite file. \nUpdate this file as you update your database.\n'''\nimport os, sys\nimport importlib\nimport datetime\n\n# Don't forget to import your own models!\nfrom app.models import *\n\nconf = load_config('app/config.yaml')\n\nsqlite_dbs  = [ conf['databases']['dev']\n                # add more here if multiple DBs\n              ]\n\n# Remove DBs\nfor fname in sqlite_dbs:\n  try:\n    print (\"Removing {0}.\".format(fname))\n    os.remove(fname)\n  except OSError:\n    pass\n\n# Creates DBs\nfor fname in sqlite_dbs:\n  if os.path.isfile(fname):\n    print (\"Database {0} should not exist at this point!\".format(fname))\n  print (\"Creating empty SQLite file: {0}.\".format(fname))\n  open(fname, 'a').close()\n  \n\ndef class_from_name (module_name, class_name):\n  # load the module, will raise ImportError if module cannot be loaded\n  # m = __import__(module_name, globals(), locals(), class_name)\n  # get the class, will raise AttributeError if class cannot be found\n  c = getattr(module_name, class_name)\n  return c\n    \n\"\"\"This file creates the database and fills it with some dummy run it after you have made changes to the models pages.\"\"\"\ndef get_classes (db):\n  classes = []\n  for str in conf['models'][db]:\n    print (\"\\tCreating model for '{0}'\".format(str))\n    c = class_from_name(sys.modules[__name__], str)\n    classes.append(c)\n  return classes\n\n  \nmainDB.create_tables(get_classes('mainDB'))\n\n#Adding dummy data\nusers = User(  firstName = \"Scott\",\n                lastName  = \"Heggen\",\n                username  = \"heggens\",\n                email     = \"heggens@berea.edu\",\n                isAdmin   = 1,\n                program   = 1\n            ).save(force_insert=True)\n            \nusers = User(  firstName = \"Jan\",\n                lastName  = \"Pearce\",\n                username  = \"pearcej\",\n                email     = \"jadudm@berea.edu\",\n                isAdmin   = 0,\n                program   = 2\n            ).save(force_insert=True)     \n\nusers = User(  firstName = \"Matt\",\n                lastName  = \"Jadud\",\n                username  = \"jadudm\",\n                email     = \"jadudm@berea.edu\",\n                isAdmin   = 0,\n                program   = 2\n            ).save(force_insert=True)\n            \nusers = User(  firstName = \"Cody\",\n                lastName  = \"Myers\",\n                username  = \"myersco\",\n                email     = \"jadudm@berea.edu\",\n                isAdmin   = 0,\n                program   = 2\n            ).save(force_insert=True)\n  \n     \n\ndivision = Division(  name = \"Division I\"\n              ).save()\n\ndivision = Division(  name = \"Division II\"\n              ).save()\n\nprogram  = Program( name = \"Computer Science\",\n                    division = 2,\n                    prefix   = \"CSC\"\n              ).save()\n              \nprogram  = Program( name = \"Mathematics\",\n                    division = 1,\n                    prefix   = \"MAT\"\n              ).save()\n             \nsubject = Subject(  prefix  = \"CSC\",\n                    pid     = 1,\n                    webname = \"cs.berea.edu\"\n                    ).save(force_insert=True)\n                    \nsubject = Subject(  prefix  = \"MAT\",\n                    pid     = 2,\n                    webname = \"math.berea.edu\"\n                  ).save(force_insert=True)\n\nbanner = BannerSchedule(  letter        = \"Standard A\",\n                          days          = \"MWF\",\n                          startTime     = datetime.time(8, 0, 0),\n                          endTime       = datetime.time(9, 10, 0),\n                          sid           = \"A\",\n                          order         = 1\n                        ).save(force_insert=True)\n\nbanner = BannerSchedule(  letter        = \"Standard B\",\n                          days          = \"MWF\",\n                          startTime     = datetime.time(9, 20, 0),\n                          endTime       = datetime.time(10, 30, 0),\n                          sid           = \"B\",\n                          order         = 2\n                        ).save(force_insert=True)\n\nbannercourse =  BannerCourses(  subject       = \"CSC\",\n                                number        = 236,\n                                ctitle        = \"Data Structures\"\n                              ).save()\n\nbannercourse =  BannerCourses(  subject       = \"MAT\",\n                                number        = 135,\n                                ctitle        = \"Calculus I\"\n                              ).save()\n\nterm = Term(  name              = \"Fall 2016\",\n              termCode          = 201611,\n              editable          = 0\n            ).save(force_insert = True)\n            \nterm = Term(  name              = \"Spring 2017\",\n              termCode          = 201612,\n              editable          = 0\n            ).save(force_insert = True)      \n            \n\ncourse = Course(  bannerRef         = 1,\n                  prefix            = \"CSC\",\n                  term              = 201611,\n                  schedule          = \"A\",\n                  capacity          = 20,\n                  notes          = \"Preference1\"\n                ).save()\n                \ncourse = Course(  bannerRef         = 2,\n                  prefix            = \"MAT\",\n                  term              = 201612,\n                  schedule          = \"B\",\n                  capacity          = 20,\n                  notes          = \"Preference2\"\n                ).save()                \n\ncourse = Course(  bannerRef         = 1,\n                  prefix            = \"CSC\",\n                  term              = 201612,\n                  schedule          = \"B\",\n                  capacity          = 20,\n                  notes          = \"Preference1\"\n                  ).save()\n                  \npchair = ProgramChair(  username  = \"jadudm\",\n                        pid       = 1\n                    ).save()\n                    \n                    \ndchair = DivisionChair(  username  = \"pearcej\",\n                        did       = 2\n                      ).save()\n\ninstructor = InstructorCourse(  username = \"heggens\",\n                                course   = 1\n                              ).save()\n                              \ninstructor = InstructorCourse(  username = \"jadudm\",\n                                course   = 2\n                              ).save()\n                              \ninstructor = InstructorCourse(  username = \"myersco\",\n                                course   = 3\n                              ).save()  ","undoManager":{"mark":-29,"position":100,"stack":[[{"start":{"row":72,"column":29},"end":{"row":72,"column":30},"action":"remove","lines":["j"],"id":58}],[{"start":{"row":72,"column":29},"end":{"row":72,"column":30},"action":"insert","lines":["M"],"id":59}],[{"start":{"row":72,"column":30},"end":{"row":72,"column":31},"action":"insert","lines":["y"],"id":60}],[{"start":{"row":72,"column":31},"end":{"row":72,"column":32},"action":"insert","lines":["e"],"id":61}],[{"start":{"row":72,"column":32},"end":{"row":72,"column":33},"action":"insert","lines":["r"],"id":62}],[{"start":{"row":72,"column":33},"end":{"row":72,"column":34},"action":"insert","lines":["s"],"id":63}],[{"start":{"row":72,"column":34},"end":{"row":72,"column":35},"action":"insert","lines":["c"],"id":64}],[{"start":{"row":72,"column":35},"end":{"row":72,"column":36},"action":"insert","lines":["o"],"id":65}],[{"start":{"row":76,"column":37},"end":{"row":76,"column":49},"action":"remove","lines":["            "],"id":66},{"start":{"row":76,"column":37},"end":{"row":77,"column":0},"action":"insert","lines":["",""]},{"start":{"row":77,"column":0},"end":{"row":77,"column":12},"action":"insert","lines":["            "]}],[{"start":{"row":77,"column":2},"end":{"row":78,"column":0},"action":"insert","lines":["",""],"id":67},{"start":{"row":78,"column":0},"end":{"row":78,"column":2},"action":"insert","lines":["  "]}],[{"start":{"row":78,"column":1},"end":{"row":78,"column":2},"action":"remove","lines":[" "],"id":68}],[{"start":{"row":78,"column":0},"end":{"row":78,"column":1},"action":"remove","lines":[" "],"id":69}],[{"start":{"row":78,"column":0},"end":{"row":84,"column":37},"action":"insert","lines":["users = User(  firstName = \"Cody\",","                lastName  = \"Myers\",","                username  = \"Myersco\",","                email     = \"jadudm@berea.edu\",","                isAdmin   = 0,","                program   = 2","            ).save(force_insert=True)"],"id":70}],[{"start":{"row":78,"column":31},"end":{"row":78,"column":32},"action":"remove","lines":["y"],"id":71}],[{"start":{"row":78,"column":30},"end":{"row":78,"column":31},"action":"remove","lines":["d"],"id":72}],[{"start":{"row":78,"column":29},"end":{"row":78,"column":30},"action":"remove","lines":["o"],"id":73}],[{"start":{"row":78,"column":28},"end":{"row":78,"column":29},"action":"remove","lines":["C"],"id":74}],[{"start":{"row":78,"column":28},"end":{"row":78,"column":29},"action":"insert","lines":["J"],"id":75}],[{"start":{"row":78,"column":29},"end":{"row":78,"column":30},"action":"insert","lines":["e"],"id":76}],[{"start":{"row":78,"column":30},"end":{"row":78,"column":31},"action":"insert","lines":["a"],"id":77}],[{"start":{"row":78,"column":30},"end":{"row":78,"column":31},"action":"remove","lines":["a"],"id":78}],[{"start":{"row":78,"column":29},"end":{"row":78,"column":30},"action":"remove","lines":["e"],"id":79}],[{"start":{"row":78,"column":29},"end":{"row":78,"column":30},"action":"insert","lines":["a"],"id":80}],[{"start":{"row":78,"column":30},"end":{"row":78,"column":31},"action":"insert","lines":["n"],"id":81}],[{"start":{"row":79,"column":33},"end":{"row":79,"column":34},"action":"remove","lines":["s"],"id":82}],[{"start":{"row":79,"column":32},"end":{"row":79,"column":33},"action":"remove","lines":["r"],"id":83}],[{"start":{"row":79,"column":31},"end":{"row":79,"column":32},"action":"remove","lines":["e"],"id":84}],[{"start":{"row":79,"column":30},"end":{"row":79,"column":31},"action":"remove","lines":["y"],"id":85}],[{"start":{"row":79,"column":29},"end":{"row":79,"column":30},"action":"remove","lines":["M"],"id":86}],[{"start":{"row":79,"column":29},"end":{"row":79,"column":30},"action":"insert","lines":["P"],"id":87}],[{"start":{"row":79,"column":30},"end":{"row":79,"column":31},"action":"insert","lines":["e"],"id":88}],[{"start":{"row":79,"column":31},"end":{"row":79,"column":32},"action":"insert","lines":["a"],"id":89}],[{"start":{"row":79,"column":32},"end":{"row":79,"column":33},"action":"insert","lines":["r"],"id":90}],[{"start":{"row":79,"column":33},"end":{"row":79,"column":34},"action":"insert","lines":["c"],"id":91}],[{"start":{"row":79,"column":34},"end":{"row":79,"column":35},"action":"insert","lines":["e"],"id":92}],[{"start":{"row":72,"column":29},"end":{"row":72,"column":30},"action":"remove","lines":["M"],"id":93}],[{"start":{"row":72,"column":29},"end":{"row":72,"column":30},"action":"insert","lines":["m"],"id":94}],[{"start":{"row":80,"column":29},"end":{"row":80,"column":36},"action":"remove","lines":["Myersco"],"id":95}],[{"start":{"row":80,"column":29},"end":{"row":80,"column":30},"action":"insert","lines":["p"],"id":96}],[{"start":{"row":80,"column":30},"end":{"row":80,"column":31},"action":"insert","lines":["e"],"id":97}],[{"start":{"row":80,"column":31},"end":{"row":80,"column":32},"action":"insert","lines":["a"],"id":98}],[{"start":{"row":80,"column":32},"end":{"row":80,"column":33},"action":"insert","lines":["r"],"id":99}],[{"start":{"row":80,"column":33},"end":{"row":80,"column":34},"action":"insert","lines":["c"],"id":100}],[{"start":{"row":80,"column":34},"end":{"row":80,"column":35},"action":"insert","lines":["e"],"id":101}],[{"start":{"row":80,"column":35},"end":{"row":80,"column":36},"action":"insert","lines":["j"],"id":102}],[{"start":{"row":78,"column":0},"end":{"row":84,"column":42},"action":"remove","lines":["users = User(  firstName = \"Jan\",","                lastName  = \"Pearce\",","                username  = \"pearcej\",","                email     = \"jadudm@berea.edu\",","                isAdmin   = 0,","                program   = 2","            ).save(force_insert=True)     "],"id":103}],[{"start":{"row":60,"column":37},"end":{"row":61,"column":0},"action":"insert","lines":["",""],"id":104},{"start":{"row":61,"column":0},"end":{"row":61,"column":12},"action":"insert","lines":["            "]}],[{"start":{"row":61,"column":12},"end":{"row":62,"column":0},"action":"insert","lines":["",""],"id":105},{"start":{"row":62,"column":0},"end":{"row":62,"column":12},"action":"insert","lines":["            "]}],[{"start":{"row":62,"column":8},"end":{"row":62,"column":12},"action":"remove","lines":["    "],"id":106}],[{"start":{"row":62,"column":4},"end":{"row":62,"column":8},"action":"remove","lines":["    "],"id":107}],[{"start":{"row":62,"column":0},"end":{"row":62,"column":4},"action":"remove","lines":["    "],"id":108}],[{"start":{"row":62,"column":0},"end":{"row":68,"column":42},"action":"insert","lines":["users = User(  firstName = \"Jan\",","                lastName  = \"Pearce\",","                username  = \"pearcej\",","                email     = \"jadudm@berea.edu\",","                isAdmin   = 0,","                program   = 2","            ).save(force_insert=True)     "],"id":109}],[{"start":{"row":170,"column":39},"end":{"row":170,"column":40},"action":"remove","lines":["A"],"id":110}],[{"start":{"row":170,"column":39},"end":{"row":170,"column":40},"action":"insert","lines":["B"],"id":111}],[{"start":{"row":176,"column":36},"end":{"row":176,"column":37},"action":"remove","lines":["1"],"id":112}],[{"start":{"row":176,"column":36},"end":{"row":176,"column":37},"action":"insert","lines":["1"],"id":113}],[{"start":{"row":179,"column":0},"end":{"row":181,"column":28},"action":"remove","lines":["pchair = ProgramChair(  username  = \"jadudm\",","                        pid       = 2","                    ).save()"],"id":114}],[{"start":{"row":178,"column":20},"end":{"row":179,"column":0},"action":"remove","lines":["",""],"id":115}],[{"start":{"row":184,"column":43},"end":{"row":184,"column":44},"action":"remove","lines":["m"],"id":116}],[{"start":{"row":184,"column":42},"end":{"row":184,"column":43},"action":"remove","lines":["d"],"id":117}],[{"start":{"row":184,"column":41},"end":{"row":184,"column":42},"action":"remove","lines":["u"],"id":118}],[{"start":{"row":184,"column":40},"end":{"row":184,"column":41},"action":"remove","lines":["d"],"id":119}],[{"start":{"row":184,"column":39},"end":{"row":184,"column":40},"action":"remove","lines":["a"],"id":120}],[{"start":{"row":184,"column":38},"end":{"row":184,"column":39},"action":"remove","lines":["j"],"id":121}],[{"start":{"row":184,"column":38},"end":{"row":184,"column":39},"action":"insert","lines":["p"],"id":122}],[{"start":{"row":184,"column":39},"end":{"row":184,"column":40},"action":"insert","lines":["e"],"id":123}],[{"start":{"row":184,"column":40},"end":{"row":184,"column":41},"action":"insert","lines":["a"],"id":124}],[{"start":{"row":184,"column":41},"end":{"row":184,"column":42},"action":"insert","lines":["r"],"id":125}],[{"start":{"row":184,"column":42},"end":{"row":184,"column":43},"action":"insert","lines":["c"],"id":126}],[{"start":{"row":184,"column":43},"end":{"row":184,"column":44},"action":"insert","lines":["e"],"id":127}],[{"start":{"row":184,"column":44},"end":{"row":184,"column":45},"action":"insert","lines":["j"],"id":128}],[{"start":{"row":180,"column":0},"end":{"row":182,"column":30},"action":"remove","lines":["dchair = DivisionChair( username  = \"jadudm\",","                        did       = 1","                      ).save()"],"id":129}],[{"start":{"row":179,"column":0},"end":{"row":180,"column":0},"action":"remove","lines":["",""],"id":130}],[{"start":{"row":178,"column":20},"end":{"row":179,"column":0},"action":"remove","lines":["",""],"id":131}],[{"start":{"row":190,"column":38},"end":{"row":190,"column":68},"action":"remove","lines":["                              "],"id":132},{"start":{"row":190,"column":38},"end":{"row":191,"column":0},"action":"insert","lines":["",""]},{"start":{"row":191,"column":0},"end":{"row":191,"column":30},"action":"insert","lines":["                              "]}],[{"start":{"row":191,"column":30},"end":{"row":192,"column":0},"action":"insert","lines":["",""],"id":133},{"start":{"row":192,"column":0},"end":{"row":192,"column":30},"action":"insert","lines":["                              "]}],[{"start":{"row":192,"column":29},"end":{"row":192,"column":30},"action":"remove","lines":[" "],"id":134}],[{"start":{"row":192,"column":28},"end":{"row":192,"column":29},"action":"remove","lines":[" "],"id":135}],[{"start":{"row":192,"column":24},"end":{"row":192,"column":28},"action":"remove","lines":["    "],"id":136}],[{"start":{"row":192,"column":20},"end":{"row":192,"column":24},"action":"remove","lines":["    "],"id":137}],[{"start":{"row":192,"column":16},"end":{"row":192,"column":20},"action":"remove","lines":["    "],"id":138}],[{"start":{"row":192,"column":12},"end":{"row":192,"column":16},"action":"remove","lines":["    "],"id":139}],[{"start":{"row":192,"column":8},"end":{"row":192,"column":12},"action":"remove","lines":["    "],"id":140}],[{"start":{"row":192,"column":4},"end":{"row":192,"column":8},"action":"remove","lines":["    "],"id":141}],[{"start":{"row":192,"column":0},"end":{"row":192,"column":4},"action":"remove","lines":["    "],"id":142}],[{"start":{"row":192,"column":0},"end":{"row":194,"column":40},"action":"insert","lines":["instructor = InstructorCourse(  username = \"jadudm\",","                                course   = 2","                              ).save()  "],"id":143}],[{"start":{"row":193,"column":43},"end":{"row":193,"column":44},"action":"remove","lines":["2"],"id":144}],[{"start":{"row":193,"column":43},"end":{"row":193,"column":44},"action":"insert","lines":["3"],"id":145}],[{"start":{"row":192,"column":49},"end":{"row":192,"column":50},"action":"remove","lines":["m"],"id":146}],[{"start":{"row":192,"column":48},"end":{"row":192,"column":49},"action":"remove","lines":["d"],"id":147}],[{"start":{"row":192,"column":47},"end":{"row":192,"column":48},"action":"remove","lines":["u"],"id":148}],[{"start":{"row":192,"column":46},"end":{"row":192,"column":47},"action":"remove","lines":["d"],"id":149}],[{"start":{"row":192,"column":45},"end":{"row":192,"column":46},"action":"remove","lines":["a"],"id":150}],[{"start":{"row":192,"column":44},"end":{"row":192,"column":45},"action":"remove","lines":["j"],"id":151}],[{"start":{"row":192,"column":44},"end":{"row":192,"column":45},"action":"insert","lines":["m"],"id":152}],[{"start":{"row":192,"column":45},"end":{"row":192,"column":46},"action":"insert","lines":["y"],"id":153}],[{"start":{"row":192,"column":46},"end":{"row":192,"column":47},"action":"insert","lines":["e"],"id":154}],[{"start":{"row":192,"column":47},"end":{"row":192,"column":48},"action":"insert","lines":["r"],"id":155}],[{"start":{"row":192,"column":48},"end":{"row":192,"column":49},"action":"insert","lines":["s"],"id":156}],[{"start":{"row":192,"column":49},"end":{"row":192,"column":50},"action":"insert","lines":["c"],"id":157}],[{"start":{"row":192,"column":50},"end":{"row":192,"column":51},"action":"insert","lines":["o"],"id":158}]]},"ace":{"folds":[],"scrolltop":697,"scrollleft":0,"selection":{"start":{"row":183,"column":0},"end":{"row":183,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":20,"state":"start","mode":"ace/mode/python"}},"timestamp":1465409745033}