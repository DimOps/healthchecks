import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db_models import Check

with open("healthchecks.json", "r") as read_file:
    data = json.load(read_file)

json_data = data['check']

engine = create_engine("sqlite:///healthchecks.db")
Session = sessionmaker(bind=engine)
session = Session()
db_data = session.query(Check).all()
# check if someone change the name but not the host and type and just state it
# raise error if someone is trying to replicate name
# raise error if someone is trying to pass one check twice or more
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