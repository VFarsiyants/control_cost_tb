from database.base import engine, Base


class HandleCommand:
    @classmethod
    def command(cls):
        from database import models
        Base.metadata.create_all(engine)
