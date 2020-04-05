[pip3 install virtualenv]
virtualenv env
source env/bin/activate
pip3 install flask flask-sqlalchemy

Must setup database manually in python ONCE, to create the db in env:
    # Type following in console:
    # python3 [enter] from app import db [enter] db.create_all() [enter] exit() [enter]