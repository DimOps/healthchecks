import hug
from extractor import db_extractor


@hug.get('/api/data')
def get_data():
    res = db_extractor()
    db_data = {'instances': [
        {
            'ping_id': db_instance.ping_id,
            'status': db_instance.status,
            'lastDownStart': db_instance.last_down_start,
            'lastDownEnd': db_instance.last_down_end
        }
        for db_instance in res]}

    return db_data
