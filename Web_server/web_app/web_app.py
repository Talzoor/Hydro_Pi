from flask import Flask
#from flask_admin import Admin
#from flask_peewee.admin import Admin
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_admin.contrib.peewee import ModelView
from flask_peewee.auth import Auth


#from flask_admin.contrib.peewee import tools
import main
import os
import models


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

print('path:{}'.format(SCRIPT_PATH))
print('db:{}'.format(main.db.database))

app = Flask(__name__)
app.config.from_object('config.Configuration')
db = Database(app)
# database = db.database

# create an Auth object for use with our flask app and database wrapper
auth = Auth(app, db)

#admin = Admin(app, name='HydroPi_test', template_mode='bootstrap3')
#admin = Admin(app, name='HydroPi_test', template_mode='bootstrap3', url='/')
#admin = Admin(app, name='HydroPi_test', index_view=AdminIndexView(main.PulseData, url='/', endpoint=''))

#admin.register(main.PulseData)

#admin.add_view(ModelView(main.PulseData))
#admin.setup()

# Add administrative views here