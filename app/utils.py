import os
from app import app

def envConfigFile():
    env = lower(os.environ['ENV']) if 'ENV' in os.environ  else 'dev'
    if env not in ['dev', 'prod']:
        env = 'dev'
    return os.path.join(app.globalPath, '%s/%s.ini' %('config', env))
