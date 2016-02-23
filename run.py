
from job import app
from flask_wtf.csrf import CsrfProtect
app.debug = app.config['DEBUG']

if __name__ == '__main__':
    print 'We are running flask via main()'
    CsrfProtect(app)
    app.run(host="0.0.0.0")