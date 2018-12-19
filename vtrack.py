from app import create_app, db
from app.models import User, Vehicle, Picture

app = create_app("development")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Vehicle": Vehicle, "Picture": Picture}
