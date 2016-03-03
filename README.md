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
Above you will find the file structure for the flask template. You will be mostly working with the app/ directory.
some important files and directories.

* models.py - This file contains the database schema or the tables and columns that will be in database.
If you want to make a new table then you will add a class to this file, see the example in the models.py file.
Once you are done making changes to this file run create_db.py to make the changes in the database.

* App/ directory - This directory will contain a python module. In order for python files to be recognized they must be added to the \_\_init\_\_.py file in this directory.

* start.py - This file is a very quick example of a python file that will render a page. This file processes and renders the start.html file located under templates.

## Example for creating a new view ##
If I wanted to create a new page with a picture on it  then I would do the following.

1. Create your python file inside of the app/ directory. Here you will include the decorator @app.route as seen in other files
```python
        from allImports import *
        @app.route("/example", methods = ["GET"])
        def example():
            return render_template("example.html", cfg = cfg)
```
2. Include this file in the \_\_init\_\_.py file.
    

## documentation links ##

* [jinja documentation](http://jinja.pocoo.org/)
* [Peewee Documentation](http://docs.peewee-orm.com/en/latest/)
* [Git documentation](https://git-scm.com/documentation)
* [Flask Documentation](http://flask.pocoo.org/docs/0.10/)