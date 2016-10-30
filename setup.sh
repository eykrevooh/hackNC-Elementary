'''
This file sets up the virtual environment.
Run "source setup.sh" each time you want to run the app.
'''

mkdir -p data

pip install Flask   --upgrade
pip install peewee  --upgrade
pip install pyyaml  --upgrade
pip install wtf-peewee
pip install watson-developer-cloud --upgrade
