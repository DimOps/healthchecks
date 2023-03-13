import hug
from hug.middleware import CORSMiddleware
from checks_crud_api import ChecksCrudApi
from utils import create_ui_obj
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Status, Check


api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))


@hug.get('/api/data')
def get_data():
    engine = create_engine("sqlite:///healthchecks.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    tuple_cls = session.query(Check, Status).filter(Check.id == Status.check_id).all()
    session.close()

    db_data = {"checks": []}

    for t in tuple_cls:
        obj = create_ui_obj(t[0], t[1])
        db_data['checks'].append(obj)
    return db_data


@hug.post('/api/summary')
def outage_summary(ping_id, **kwargs):
    """
    Default report span is 7 days back in time.
    :param ping_id: id from Pingdom which feeds into their APIs
            kwargs: from - date in UNIX time format
                    to - date in UNIX time format
    :return: time in MINUTES from the set time to now for each status type
    """
    resp_summary = ChecksCrudApi().get_check_outage_summary(ping_id, **kwargs)
    report = {'unknown': 0, 'up': 0, 'down': 0}

    # extracts time in minutes to calculate percentage on the client
    for stamp in resp_summary['summary']['states']:
        if stamp['status'] == 'unknown':
            report['unknown'] += (stamp['timeto'] - stamp['timefrom'])/60
        elif stamp['status'] == 'up':
            report['up'] += (stamp['timeto'] - stamp['timefrom']) / 60
        elif stamp['status'] == 'down':
            report['down'] += (stamp['timeto'] - stamp['timefrom'])/60

    return report