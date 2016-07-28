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

# needed to migrate the cas.sql
pip install MySQL-python
