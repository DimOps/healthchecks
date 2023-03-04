import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Check

with open("healthchecks.json", "r") as read_file:
    data = json.load(read_file)

json_data = data['check']

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
db_data = session.query(Check).all()

deletions = []
for db_instance in db_data:
    eq = False
    for obj in json_data:
        if not (obj['host'] == db_instance.host
                and
                obj['type'] == db_instance.type):
            continue
        else:
            json_data.remove(obj)
            eq = True
            break
    if eq is False:
        deletions.append(db_instance)


[session.delete(inst) for inst in deletions]
session.commit()

session.add_all([Check(name=obj['name'],
                       host=obj['host'],
                       type=obj['type'])
                 for obj in json_data])

session.commit()
session.close()