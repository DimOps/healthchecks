from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create_db_models import Status


def db_extractor():
    engine = create_engine("sqlite:///healthchecks.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(Status).all()
    session.close()

    return data
