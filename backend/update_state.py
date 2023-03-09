from create_db_models import Status
from checks_crud_api import ChecksCrudApi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def change_record(check, ping):
    if check.ping_id != ping['id']:
        raise Exception('Status table IDs does NOT match Pingdom IDs! Sync data!')
    else:
        ping_dict_stats = dict((key, value) for (key, value) in ping.items()
                               if key == 'status'
                               or key == 'lastdownstart'
                               or key == 'lastdownend')

        db_status_record = {'status': check.status,
                            'lastdownstart': check.lastdownstart,
                            'lastdownend': check.lastdownend}

        for k, v in ping_dict_stats.items():
            if ping_dict_stats[k] != db_status_record[k]:
                u = {f'{k}': ping_dict_stats[k]}
                print(u)
                session.query(Status).filter(Status.ping_id == ping['id']).update(u)
        session.commit()


def update_state():
    checks_list = session.query(Status).all()
    pings_list = ChecksCrudApi().get_checks_list()

    [change_record(c, p) for c, p in zip(checks_list, pings_list['checks'])
     if c.status != p['status']
     or c.ping_id != p['id']]


update_state()
session.close()

