from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Check, Status


def to_create_checks():
    engine = create_engine("sqlite:///healthchecks.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    checks = session.query(Check).all()
    current_checks = session.query(Status).all()
    session.close()

    for c_check in current_checks:
        for check in checks:
            if c_check.check_id == check.id:
                checks.remove(check)
                break

    return [{"name": f"{c.name}",
             "host": f"{c.host}",
             "type": f"{c.type}"} for c in checks]
