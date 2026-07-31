from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# We create these here (not inside app/__init__.py) so other files
# can import them without causing circular-import errors.
db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()