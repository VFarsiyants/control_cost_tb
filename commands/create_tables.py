from database.connection import engine
from database.models import Base


class HandleCommand:
    @classmethod
    def command(cls):
        Base.metadata.create_all(engine)
