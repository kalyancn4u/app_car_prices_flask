"""Entry point for production WSGI servers.

The production Dockerfile runs this app via gunicorn:

    gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app

`wsgi:app` means "import the module wsgi.py and use its `app` object" — that
object is the same Flask() instance defined in app.py, just re-exported here
under the conventional name gunicorn (and most WSGI hosts) expect to find.
"""

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
