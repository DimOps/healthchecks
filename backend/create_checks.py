from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Check, Status
from checks_crud_api import ChecksCrudApi

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def _to_create_checks():
    checks_list = session.query(Check).all()
    added_checks = session.query(Status).all()

    for c_check in added_checks:
        for check in checks_list:
            if c_check.check_id == check.id:
                checks_list.remove(check)
                break

    return [{
         "id": f"{c.id}",
         "obj": {
            "name": f"{c.name}",
            "host": f"{c.host}",
            "type": f"{c.type}"}
             }
            for c in checks_list]


def create_checks(**kwargs):
    if not kwargs:
        data = _to_create_checks()
    else:
        res = ChecksCrudApi.create_check(kwargs['obj'])
        session.add(Status(ping_id=res['check']['id'], check_id=kwargs['check_id']))
        session.commit()
        stat_record = session.query(Status).get(res['check']['id'])
        return stat_record

    for obj in data:
        to_create = obj['obj']
        res = ChecksCrudApi.create_check(to_create)
        # include try-catch
        check_id = int(obj['id'])
        ping_id = int(res['check']['id'])
        session.add(Status(ping_id=ping_id, check_id=check_id))
    session.commit()
    session.close()
    return True  # confirmation

