import sys
sys.path.insert(0, '/var/html/www/py/goodjob/online')
from werkzeug.contrib.fixers import ProxyFix # needed for http server proxies
from werkzeug.debug import DebuggedApplication
from flask_wtf.csrf import CsrfProtect
from job import app # as application

app.wsgi_app = ProxyFix(app.wsgi_app) # needed for http server proxies
application = DebuggedApplication(app, True)
CsrfProtect(app)
