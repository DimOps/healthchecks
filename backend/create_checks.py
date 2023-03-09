from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Status
from checks_crud_api import ChecksCrudApi

engine = create_engine("sqlite:///healthchecks.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def data_transformation(checks_list):
    return [{
         "id": f"{c.id}",
         "obj": {
            "name": f"{c.name}",
            "host": f"{c.host}",
            "type": f"{c.type}"}
             }
            for c in checks_list]


def create_checks(data):
    """
    Called when JSON file updated, hence "checks" table expanded.
    create_checks function follows the good practice
    to first successfully create tangible object on
    third party servers and then insert the record in DB.

    :param data: checks in "checks" DB table without 'checking'
                connection with "status" table
    """

    transformed_data = data_transformation(data)

    for obj in transformed_data:
        to_create_ping = obj['obj']
        res = ChecksCrudApi().create_check(to_create_ping)
        check_id = int(obj['id'])
        ping_id = int(res['check']['id'])
        session.add(Status(ping_id=ping_id, check_id=check_id))

    session.commit()
    session.close()

