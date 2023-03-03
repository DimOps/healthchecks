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

Session = sessionmaker(bind=engine)
session = Session()
session.add_all(
    [
        Check(name="sap", host="www.sap.com", type="http"),
        Check(name="amazon", host="www.aws.com", type="http"),
    ]
)

session.commit()

for name, host in session.query(Check.name, Check.host):
    print(name, host)

session.close()