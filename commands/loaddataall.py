from glob import glob
from pathlib import Path
import json
from itertools import groupby

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import bindparam

from database.models import Base
from database.connection import Session

class HandleCommand:
    @classmethod
    def command(cls):
        fixtures_path = Path('database', 'fixtures', '*.json')
        fixtures_list = glob(str(fixtures_path))
        record_list = list()
        for file in fixtures_list:
            with open(file, 'r', encoding='utf-8') as f:
                record_list.extend(json.load(f))
        grouper = lambda item: item['model']
        record_list = sorted(record_list, key=grouper)
        with Session.begin() as session:
            for model, group_items in groupby(record_list, key=grouper):
                group_items = list(group_items)
                table = Base.metadata.tables[model]
                # Inserting not existed, new records from fixtures
                insert_stmt = insert(table).values([
                    {
                        'id': item['pk'],
                        **item['fields']
                    } for item in group_items
                ]).on_conflict_do_nothing()
                session.execute(insert_stmt)

                # Updating old records of fixtures
                bind_dict = {
                    key: bindparam(key) for key 
                    in group_items[0]['fields'].keys()
                }
                stmt = table.update().\
                    where(table.c.id == bindparam('_id')).\
                    values(bind_dict)
                session.execute(
                    stmt, [
                        {'_id':item['pk'], **item['fields']} for item 
                        in group_items
                    ]
                )
