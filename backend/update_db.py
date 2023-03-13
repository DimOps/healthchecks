import json
from collections import Counter
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

stringified_checks = [f"{hc['name']} - {hc['host']} - {hc['type']}" for hc in json_data]
residuals = [item for item, count in Counter(stringified_checks).items() if count > 1]

if len(residuals) > 0:
    res = '\n'.join(residuals)
    raise Exception(f'Checks with the following "name - host - type" configuration are duplicated:\n{res}')

json_checks_name = [c['name'] for c in json_data]
eq_names = [item for item, count in Counter(json_checks_name).items() if count > 1]

if len(eq_names) > 0:
    names_str = ', '.join([n for n in eq_names])
    raise Exception(f'Check/s have the following names duplicated: {names_str}')

host_type_pairs = [f"{hc['host']} - {hc['type']}" for hc in json_data]
residuals = [item for item, count in Counter(stringified_checks).items() if count > 1]

if len(residuals) > 0:
    res = '\n'.join(residuals)
    print(f'The following host - type pairs have been duplicated with unique names:\n{res}')

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