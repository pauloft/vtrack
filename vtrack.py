# from werkzeug.debug import DebuggedApplication

from app import create_app, db
from app.models import User, Vehicle, Picture

app = create_app("development")

# if app.debug:
# app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Vehicle": Vehicle, "Picture": Picture}
