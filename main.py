from app import run_app
from werkzeug.serving import run_simple


if __name__ == "__main__":
    app = run_app()

    run_simple('localhost', 5000, app, ssl_context='adhoc', processes=2)
