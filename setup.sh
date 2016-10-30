'''
This file sets up the virtual environment.
Run "source setup.sh" each time you want to run the app.
'''

mkdir -p data

if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

pip install Flask   --upgrade
pip install peewee  --upgrade
pip install pyyaml  --upgrade
pip install wtf-peewee
pip install watson-developer-cloud --upgrade
