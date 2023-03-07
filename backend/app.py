import hug
from extractor import db_extractor
from checks_crud_api import ChecksCrudApi
from utils import create_ui_obj


@hug.get('/api/data')
def get_data():
    checks_list = db_extractor('Check')
    status_list = db_extractor('Status')
    db_data = {"checks": []}
    for check in checks_list:
        for stat in status_list:
            if check.id == stat.check_id:
                obj = create_ui_obj(check, stat)
                db_data['checks'].append(obj)
                break
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