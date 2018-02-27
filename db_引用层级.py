extensions.py   # doremi.extensions.py
db = SQLAlchemy()


databases.py    # doremi.databases.py
from .extensions import db

school.py   # doremi.models.school.py
from .databases.py import db


doremi.models.init.py # doremi.models.init
from .school import db


stat_command.py # doremi.commands.stat_command
from doremi.models.init.py import db