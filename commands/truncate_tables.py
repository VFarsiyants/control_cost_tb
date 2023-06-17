from sqlalchemy import text
from database.connection import Session
from database.models import Base


class HandleCommand:
    @classmethod
    def command(cls):
        tables_names = Base.metadata.tables.keys()
        with Session.begin() as session:
            for table in tables_names:
                truncate_command = text(
                    f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;'
                )
                session.execute(truncate_command)
            session.commit()
