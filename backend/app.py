import hug
from hug.middleware import CORSMiddleware
from checks_crud_api import ChecksCrudApi
from utils import create_ui_obj, outage_in_percentage
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
def outage_summary(checkId, kwargs):
    # put state changes stat in response
    # put discrepancy/ies of asked and provided by Pingdom API status report in response, if any
    """
    Default report span is 7 days back in time.
    :param checkId: id from Pingdom which feeds into their APIs
            kwargs: from - date in UNIX time format
                    to - date in UNIX time format
    :return: time in PERCENTAGE from the set time to now for each status type
    """
    time_from = kwargs['timefrom']
    time_to = kwargs['timeto']

    resp_summary = ChecksCrudApi().get_check_outage_summary(check_id=checkId, **kwargs)
    reports = resp_summary['summary']['states']

    report = {'unknown': 0, 'up': 0, 'down': 0}
    for i in range(len(reports)):
        if reports[i]['timefrom'] <= time_from <= reports[i]['timeto']:
            if time_to <= reports[i]['timeto']:
                report[reports[i]['status']] += time_to - time_from
                break
            else:
                report[reports[i]['status']] += reports[i]['timeto'] - time_from
                if i == len(reports) - 1:
                    report['unknown'] = time_to - reports[i]['timeto']
                else:
                    continue
        if time_from < reports[i]['timefrom'] and reports[i]['timeto'] < time_to:
            report[reports[i]['status']] += reports[i]['timeto'] - reports[i]['timefrom']
            if i == len(reports) - 1:
                report['unknown'] = time_to - reports[i]['timeto']
            else:
                continue
        if time_from < reports[i]['timefrom'] and time_to <= reports[i]['timeto']:
            report[reports[i]['status']] += time_to - reports[i]['timefrom']
            break

    outage = outage_in_percentage(report)

    return outage