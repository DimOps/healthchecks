from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Status, Check


def db_extractor(classname):
    engine = create_engine("sqlite:///healthchecks.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    if classname == 'Check':
        data = session.query(Check).all()
        session.close()
        return data
    elif classname == 'Status':
        data = session.query(Status).all()
        session.close()
        return data
