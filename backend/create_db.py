from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///healthchecks.db", echo=True)
Base = declarative_base()


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    host = Column(String(300))
    type = Column(String(300))

    def __repr__(self):
        return "<Check(name'%s', host='%s', type='%s')>" % (
            self.name,
            self.host,
            self.type,
        )


Base.metadata.create_all(engine)
