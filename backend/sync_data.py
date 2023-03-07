from extractor import db_extractor
from create_checks import create_checks
from utils import create_ui_obj
from checks_crud_api import ChecksCrudApi


def sync_ping():
    """
    Synchronises records in Pingdom with the
    required records in the DB. Checks Status table
    as it assumes that:
        1. update_db.py will run at each json
        amendment and
        2. One-to-One deletes cascade in DB
    """
    db_state = db_extractor('Status')
    ping_checks = ChecksCrudApi().get_checks_list()

    # assumes that only the script will interact with Pingdom APIs
    if len(db_state) >= ping_checks['counts']['total']:
        return 'Ping is synced'
    else:
        ping_instances = ping_checks['checks']
        for stat in db_state:
            for ping in ping_instances:
                if stat.ping_id == ping['id']:
                    ping_instances.remove(ping)
                    break

        ChecksCrudApi().delete_many_checks([ping['id'] for ping in ping_instances])


def sync_db():
    """
    Synchronises the data between the Check table
    and Status table which is to be current
    Pingdom statistics in the database
    """
    # Always execute sync_ping() before as
    # it will duplicate old records
    checks_list = db_extractor('Check')
    status_list = db_extractor('Status')
    db_data = {"checks": []}
    for check in checks_list:
        for stat in status_list:
            if check.id == stat.check_id:
                obj = create_ui_obj(check, stat)
                db_data['checks'].append(obj)
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
        ping_res = create_checks(**ch)
        obj = create_ui_obj(check, ping_res)
        db_data['checks'].append(obj)

    return db_data


r = sync_ping()
