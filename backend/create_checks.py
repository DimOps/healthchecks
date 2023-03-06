from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Check, Status
from checks_crud_api import ChecksCrudApi

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def to_create_checks():
    checks = session.query(Check).all()
    current_checks = session.query(Status).all()

    for c_check in current_checks:
        for check in checks:
            if c_check.check_id == check.id:
                checks.remove(check)
                break

    return [{
         "id": f"{c.id}",
         "obj": {
            "name": f"{c.name}",
            "host": f"{c.host}",
            "type": f"{c.type}"}
             }
            for c in checks]


def create_checks():
    data = to_create_checks()

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

