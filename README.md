[TOC]
#install#
## requirements ##
* python 2.7
* linux, unix, mac, windows(with attachments)
* git 

## Creating Development Environment ##
If working on a local machine then **Fork**, rename to project name and clone.

``` bash
git clone https://username@bitbucket.org/username/repositoryname.git
source setup.sh
python app.py
```
you can check your localhost to see if it deployed correctly.
if working on a c9 account follow instructions [here](https://docs.google.com/document/d/17GK7uKqdma5DMnHZXlMJwnAn63HdU9446fV1lAcxxus/edit)
``` bash
source setup.sh
python app.py
``` 
if you are succesful you can point to 0.0.0.0:8080

# Working with the flask template #
## File Hierarchy ##
```
- Project Name
   - App
      -static
      -templates
        -start.html
      - __init__.py
      - allImports.py
      - config.yaml
      - models.py
      - start.py # this an example of a python file that renders a page
   - Data
       - db.sqlite
   - Venv
   - app.py
   - create_db.py
   - setup.sh
```

## documentation links ##

* [jinja documentation](http://jinja.pocoo.org/)
* [Peewee Documentation](http://docs.peewee-orm.com/en/latest/)
* [Git documentation](https://git-scm.com/documentation)
* [Flask Documentation](http://flask.pocoo.org/docs/0.10/)