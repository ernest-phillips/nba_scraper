import json
from sqlalchemy import create_engine
from storage import schema

config=json.loads(open('config.json').read())
username = config['username']
password = config['password']
host = config['host']
database = config['database']

engine = create_engine('mysql://'+username+':'+password+'@'+host)
engine.execute("CREATE DATABASE "+database)
engine.execute("USE "+database)

schema.metadata.create_all(engine)
