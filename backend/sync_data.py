from create_db_models import Status
from extractor import db_extractor
from create_checks import create_checks
from checks_crud_api import ChecksCrudApi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def sync_ping():
    """
    Synchronises records in Pingdom with the
    required records in the DB. Checks Status table
    as it assumes that:
        1. update_db.py will run at each json
        amendment and
        2. One-to-One deletes cascade in DB
    """
    engine = create_engine("sqlite:///healthchecks.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    status_state = session.query(Status.ping_id).all()
    cs = set([int(str(p)[1:len(str(p)) - 2]) for p in status_state])

    pings_state = ChecksCrudApi().get_checks_list()
    ps = set([pc['id'] for pc in pings_state['checks']])

    to_delete = cs.difference(ps)

    ChecksCrudApi().delete_many_checks(to_delete)


def sync_db():
    """
    Synchronises the data between the Check table
    and Status table which is to be current
    Pingdom statistics in the database
    """
    # Always execute sync_ping() before as
    # it will duplicate old records(? break was bug, check)
    checks_list = db_extractor('Check')
    status_list = db_extractor('Status')

    for check in checks_list:
        for stat in status_list:
            if check.id == stat.check_id:

                status_list.remove(stat)
                break
        ch = {
            "check_id": check.id,
            "obj":
                {
                    "name": f"{check.name}",
                    "host": f"{check.host}",
                    "type": f"{check.type}"
                }
        }
        create_checks(**ch)
