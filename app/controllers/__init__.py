import glob, os

controllers = []

directoryOfThisFile = os.path.dirname(os.path.realpath(__file__))

for file in glob.glob(directoryOfThisFile + "/*Controller.py"):
    controllers.append(os.path.splitext(os.path.basename(file))[0])

__all__ = controllers
    
