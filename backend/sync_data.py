from create_db_models import Status, Check
from create_checks import create_checks
from checks_crud_api import ChecksCrudApi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)


def sync_ping():
    """
    Synchronises records in Pingdom with the
    required records in the DB. Checks Status table
    as it assumes that:
        1. update_db.py will run at each json
        amendment and
        2. One-to-One deletes cascade in DB
    """

    session = Session()

    status_state = session.query(Status.ping_id).all()
    session.close()
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

    session = Session()
    checks_list = session.query(Check).filter_by(current_state=None).all()
    session.close()
    create_checks(checks_list)


engine.dispose(close=True)
